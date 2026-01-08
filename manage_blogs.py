from server import server
from models import db, Blog
import math


def estimate_read_time(text):
    """
    Estimate reading time based on average reading speed.

    This is an approximation used widely in blogs.
    It helps users decide whether they have time to read an article,
    not to measure actual reading speed (which varies per person).
    math.ceil round up e.g 3 min read instead of 2.1 min read
    """
    if not text:
        return None

    words = len(text.split())
    minutes = math.ceil(words / 200)
    return f"{minutes} min read"


def clear_blogs():
    """
    To delete all existing blog rows.
    I need this when resetting content during development.
    """
    Blog.query.delete()
    db.session.commit()


def upsert_blog(
    slug,
    card_position,
    title,
    meta,
    summary,
    content,
    published=True
):
    """
    Insert or update a blog post.

    Uses slug as a stable identifier so the script
    can be safely re-run without creating duplicates.
    """

    blog = Blog.query.filter_by(slug=slug).first()

    read_time = estimate_read_time(content)

    if blog:
        blog.card_position = card_position
        blog.title = title
        blog.meta = meta
        blog.summary = summary
        blog.content = content
        blog.read_time = read_time
        blog.published = published
    else:
        blog = Blog(
            slug=slug,
            card_position=card_position,
            title=title,
            meta=meta,
            summary=summary,
            content=content,
            read_time=read_time,
            published=published
        )
        db.session.add(blog)


def main():
    """
    Entry point for managing blog content.
    """

    with server.app_context():
        clear_blogs()

        upsert_blog(
            slug="engineering-with-ai-is-still-engineering",
            card_position=1,
            title="Engineering With AI Is Still Engineering",
            meta="Software Engineering • Artificial Intelligence • 2026",
            summary="AI tools are changing how software is built, but engineering judgment and responsibility still matter.",
            content="""AI tools are now part of my daily development workflow. From generating boilerplate to explaining unfamiliar code, they reduce friction and speed up iteration.

Used well, AI acts as a productivity multiplier. Used poorly, it can hide weak thinking behind confident output. This makes human judgment more important, not less.

The World Economic Forum highlights that as artificial intelligence becomes more embedded in society, human oversight, accountability, and responsibility become even more critical.


At the same time, long-lived software systems rely on engineering practices that do not change quickly. Google’s Software Engineering at Google outlines principles around code ownership, documentation, and review that remain relevant today.


Read more here:
<a href="https://www.weforum.org/stories/artificial-intelligence/"
   target="_blank" rel="noopener">
https://www.weforum.org/stories/artificial-intelligence/
</a>


AI changes how we build software, not why we build it. Engineers still own the decisions, trade-offs, and outcomes. How do you decide when automation helps and when it gets in the way?
"""
        )

        upsert_blog(
            slug="reading-code-is-the-most-underrated-engineering-skill",
            card_position=2,
            title="Reading Code Is the Most Underrated Engineering Skill",
            meta="Engineering Culture • Career Growth",
            summary="Understanding existing systems matters more than writing new code in modern software teams.",
            content="""Early in my career, progress felt tied to how much code I could write. Over time, I learned that most real engineering work happens inside existing systems.

Modern engineering teams spend far more time maintaining and evolving code than creating it from scratch. Companies operating at scale consistently emphasise system understanding and long-term maintainability.


Reading code means understanding why something exists, not just what it does. Business constraints, performance trade-offs, and historical decisions are often invisible without careful analysis.

Foundational engineering guidance reinforces this idea. Google’s long-standing practices focus on readability, ownership, and knowledge sharing as essential to sustainable systems.


Read more here: <a href="https://stripe.com/blog/engineering"
   target="_blank" rel="noopener">
https://stripe.com/blog/engineering
</a>


AI can generate code instantly, but it cannot explain intent or context. Engineers who can read and reason about existing systems bring long-term value. Which skill are you deliberately practising today?
"""
        )

        upsert_blog(
            slug="why-shipping-beats-perfect-side-projects",
            card_position=3,
            title="Why Shipping Beats Perfect Side Projects",
            meta="Career Growth • Software Engineering",
            summary="Shipping small, imperfect projects teaches more than endlessly refining ideas that never leave your laptop.",
            content="""I have started more side projects than I have shipped. Each one taught me something, but the biggest lessons came from the projects that actually went live.

Modern product teams emphasise learning through iteration. Releasing work early exposes real constraints around usability, performance, and maintainability.
The hardest lessons appear after release, when users interact with your work in unexpected ways. This is where engineering decisions meet reality.

Foundational software engineering practice reinforces this mindset. Incremental change, feedback, and ownership improve systems far more effectively than perfection upfront.


Read more here:
<a href="https://martinfowler.com/articles/continuousIntegration.html"
   target="_blank" rel="noopener">
https://martinfowler.com/articles/continuousIntegration.html
</a>


Shipping builds confidence, accountability, and momentum. Perfect ideas rarely teach as much as imperfect releases. What could you ship this month if you stopped waiting?
"""
        )

        upsert_blog(
            slug="why-i-write-documentation-even-when-no-one-is-watching",
            card_position=4,
            title="Why I Write Documentation Even When No One Is Watching",
            meta="Engineering Practice • Communication • Growth",
            summary="Writing documentation for small projects builds habits that scale to real-world software teams.",
            content="""Most of my side projects will never have real users. Some will never leave my local machine. I still write documentation for all of them.

Modern engineering organisations increasingly treat documentation as part of the product. Clear written context improves onboarding, collaboration, and long-term maintainability.

Documentation exposes unclear thinking. If something is hard to explain, it is often poorly designed. Writing forces decisions to become explicit.
This principle is reinforced by long-standing engineering guidance. Sustainable teams rely on shared understanding, not just individual knowledge.


Read more here:
<a href="https://medium.com/swinginc/documentation-what-is-still-missing-in-your-project-docs-frontend-developers-perspective-24fbe578a90a"
   target="_blank" rel="noopener">
https://medium.com/swinginc/documentation-what-is-still-missing-in-your-project-docs-frontend-developers-perspective-24fbe578a90a
</a> 


Side projects are training grounds. Writing documentation builds habits that transfer directly to professional teams. How would your last project feel if someone else had to maintain it tomorrow?
"""
        )

        db.session.commit()
        print("Blog content updated successfully")


if __name__ == "__main__":
    main()
