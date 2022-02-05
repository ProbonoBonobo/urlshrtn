from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app():
    """
    Construct the core application. Must say, I kind of forgot
    what a drag it is to use Flask-SQLAlchemy instead of SQLAlchemy
    directly, but here we go.
    :return:
    """
    app = Flask(__name__, instance_relative_config=False, static_folder='static', template_folder='templates')
    app.config.from_pyfile("config.cfg")
    # db.drop_all()
    db.init_app(app)

    urls = [
        "https://www.washingtonpost.com/technology/2022/02/02/facebook-earnings-meta/",
        "https://www.linkedin.com/posts/hire-jiawei-wang_hi…am-ready-for-my-activity-6894943241523875840-tZ7C",
        "https://twitter.com/Tweetermeyer/status/1488673180403191808",
        "https://deepmind.com/blog/article/Competitive-programming-with-AlphaCode",
        "https://blockworks.co/in-second-largest-defi-hack-ever-blockchain-bridge-loses-320m-ether/",
        "https://twitter.com/spakhm/status/1489480845979095040",
        "https://www.leemeichin.com/posts/yes-i-can-connect-to-a-db-in-css.html",
        "https://reviewbunny.app/blog/dont-make-me-think-or-why-i-switched-to-rails-from-javascript-spas",
        "https://www.nasdaq.com/articles/facebook-parent-me…s-shares-tank-20-on-q4-earnings-miss-weak-outlook",
        "https://johnnyrodgers.is/building-a-modern-home",
        "https://www.reuters.com/technology/exclusive-iphon…ed-by-second-israeli-spy-firm-sources-2022-02-03/",
        "https://www.iccl.ie/news/gdpr-enforcer-rules-that-iab-europes-consent-popups-are-unlawful/",
        "https://linear.app/blog/settings-are-not-a-design-failure",
        "https://9to5mac.com/2022/02/04/apple-will-charge-2…g-alternative-payment-systems-in-the-netherlands/",
        "https://www.wired.com/story/north-korea-hacker-internet-outage/",
        "https://www.economist.com/the-economist-explains/2022/02/03/how-apples-privacy-push-cost-meta-10bn",
        "http://www.slackware.com/releasenotes/15.0.php",
        "https://blog.postman.com/postman-now-supports-grpc/",
        "https://www.npr.org/2022/02/03/1077392791/a-satellite-finds-massive-methane-leaks-from-gas-pipelines",
        "https://trungphan.substack.com/p/why-is-linkedin-so-cringe",
        "https://www.darkpattern.games",
        "https://www.nature.com/articles/s41467-021-27317-1",
        "https://pragprog.com/titles/mrpython/portable-python-projects/",
        "https://tech.nextroll.com/blog/dev/2022/02/02/rustenstein.html",
        "https://www.jremissing.com/",
        "https://github.com/reactjs/reactjs.org/issues/3896",
        "https://benhoyt.com/writings/go-version-performance/",
        "https://amitp.blogspot.com/2022/02/non-consensual-personalization.html",
        "https://www.theverge.com/2022/2/3/22915715/nintendo-earnings-q3-2021-switch-sales-forecast",
    ]

    with app.app_context():
        from urlshorten import routes  # Import routes
        from urlshorten import models  # Import models

        try:

            db.create_all()  # Create sql tables for our data models
            for url in urls:
                try:
                    db.session.add(models.Url(url))
                    db.session.commit()
                except Exception as e:
                    print(e.__class__.__name__, e)
                    db.session.rollback()
                    print(f"Error adding url {url}")
        except:
            pass
        return app


# app = init_app()
# app.app_context().push()
