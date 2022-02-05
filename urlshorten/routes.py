"""
routes.py
This is the main file for the urlshorten application. In addition to initializing the application, it also defines the
routes for the application.
"""
from urlshorten.models import Url
from urlshorten import init_app, db
from urlshorten.crud import get_short_url, get_long_url
from urlshorten.utils import urlify
from url_normalize import url_normalize as canonical
from flask import (
    render_template,
    jsonify,
    request,
    redirect,
    make_response,
)

app = init_app()


@app.route("/")
def index():
    """A convenient tabular view of all shortened urls/targets currently in the database.
    TODO: Add pagination. This will quickly become a problem for large databases.
    """
    index = Url.query.all()
    return render_template("index.html", urls=index)


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """
    This endpoint is used to shorten a url. It expects a json payload with a url key. Here's an example:
    ```
    (urlshorten-nEPT0ldB-py3.10)  kz@aoristos  ~/projects/urlshorten  http POST http://localhost:8080/api/shorten url=https://yahoo.com
    HTTP/1.0 200 OK
    Content-Length: 119
    Content-Type: application/json
    Date: Sat, 05 Feb 2022 11:28:19 GMT
    Server: Werkzeug/2.0.2 Python/3.10.1

    {
        "canonical": "https://yahoo.com/",
        "error": null,
        "input": "https://yahoo.com",
        "short_url": "IoZFM5O5"
    }
    ```
    :return: A json response with the canonical url and the shortened url. All responses obey the same 4-key schema.
    """
    long_url = request.json["url"]
    if not long_url.strip():
        return make_response(
            jsonify(
                {
                    "error": "No url provided",
                    "input": long_url,
                    "canonical": None,
                    "short_url": None,
                }
            ),
            400,
        )
    try:
        canonical_url = canonical(long_url)
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "error": f"Invalid url: {canonical_url}",
                    "input": long_url,
                    "canonical": None,
                    "short_url": None,
                }
            ),
            400,
        )
    short_url = get_short_url(canonical_url)
    if short_url:
        return make_response(
            jsonify(
                {
                    "error": None,
                    "input": long_url,
                    "canonical": canonical_url,
                    "short_url": urlify(short_url),
                }
            ),
            200,
        )
    else:
        url = Url(long_url)
        db.session.add(url)
        db.session.commit()
        return jsonify(
            {
                "error": None,
                "input": long_url,
                "canonical": canonical_url,
                "short_url": urlify(url.key),
            }
        )


@app.route("/<short_url>", methods=["GET"])
def get_target_and_redirect(short_url: str):
    """
    This endpoint is used to redirect a shortened url to its target. It leverages the memoization of the get_long_url function in
    `crud.py` to reduce the number of database queries.
    """
    try:
        target = get_long_url(short_url)
    except Exception as e:
        print(e.__class__.__name__)
        return render_template("404.html")
    print(f"{target=}")
    return (
        redirect(target)
        if target
        else render_template("404.html", url=urlify(short_url))
    )


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
