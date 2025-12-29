from server import server
from models import db, Blog
import math


def estimate_read_time(text):
    """
    Estimate reading time based on average reading speed.

    This is an approximation used widely in blogs.
    It helps users decide whether they have time to read an article,
    not to measure actual reading speed (which varies per person).
    math.ceil round up e.g 3 min read” instead of “2.1 min read”
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

    # Reading time is calculated from the article content.
    # This is done here so it is calculated once and stored,
    # rather than recalculated on every page request.
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
            slug="women-in-tech-why-it-matters",
            card_position=1,
            title="More women in tech, and why it matters beyond diversity",
            meta="Women in Tech • Industry • Real-world impact",
            summary="This is not about quotas or optics. It is about building better products, teams, and technology.",
            content="""The technology sector shapes how we work, communicate, and live. Yet for decades, it has been built largely by a narrow demographic, leading to products and systems that often overlook large parts of society.

Increasing the number of women in tech is not a branding exercise. It is a practical response to real problems. Diverse teams identify risks earlier, design more inclusive systems, and challenge assumptions that homogeneous teams often miss.

From my own experience working with learners and professionals, women entering tech often bring strengths that are undervalued in traditional tech culture: attention to detail, thoughtful problem-solving, and a strong sense of responsibility for how systems affect people.

This is not about replacing one group with another. It is about recognising that better technology comes from broader perspectives. When women are included at every level, from education to leadership, the quality and impact of technology improves for everyone."""
        )

        upsert_blog(
            slug="confidence-is-a-technical-skill",
            card_position=2,
            title="Confidence is a technical skill, not a personality trait",
            meta="Learning • Careers • Growth mindset",
            summary="Confidence grows through practice, feedback, and problem-solving, not bravado or natural talent.",
            content="""Confidence is often misunderstood as something you either have or do not. In reality, confidence is built the same way technical skill is built: through repetition, feedback, and reflection.

In technology, progress rarely comes from instant success. It comes from trying, failing safely, understanding why something did not work, and trying again. People who appear confident are often those who have learned how to navigate uncertainty without shutting down.

This applies well beyond coding. Whether learning a new tool, changing careers, or returning to education later in life, confidence grows when progress is visible and achievable.

Creating environments where mistakes are treated as part of learning rather than evidence of failure changes outcomes dramatically. When people are supported to ask questions, test ideas, and refine their thinking, confidence follows naturally.

Confidence is not about being loud. It is about trusting your ability to figure things out."""
        )

        # Article 3: Adults, parents, professionals, AI literacy
        upsert_blog(
            slug="generative-ai-responsibility",
            card_position=3,
            title="Generative AI is powerful, but responsibility matters more",
            meta="Artificial Intelligence • Ethics • Digital responsibility",
            summary="AI tools can support productivity and learning, but only when used critically and responsibly.",
            content="""Generative AI tools are now part of everyday life, from writing assistance to code generation. Their accessibility makes them powerful, but also risky when misunderstood.

These systems do not think or understand. They predict patterns based on data. This means they can produce responses that sound confident while being incorrect, biased, or inappropriate for the context.

For adults, professionals, and parents, the key skill is not learning how to prompt an AI tool, but learning how to question its output. Verification, accountability, and ethical judgement remain human responsibilities.

There are also important considerations around data privacy and security. Sharing sensitive information with AI systems can expose data in unintended ways if safeguards are not understood.

AI literacy is now a life skill. Used well, these tools can enhance productivity and creativity. Used carelessly, they can undermine trust, accuracy, and safety. The difference lies in education and awareness, not the technology itself. If you would like to read further about using AI safely and responsibly, the following resources are useful starting points:

<a href="https://www.oecd.org/en/topics/sub-issues/ai-risks-and-incidents.html"
   target="_blank" rel="noopener">
https://www.oecd.org/en/topics/sub-issues/ai-risks-and-incidents.html
</a>
"""
        )


        upsert_blog(
            slug="exam-technique-and-stress",
            card_position=4,
            title="Exam technique that gets results without burning out",
            meta="GCSE • A Level • Exam technique • Managing stress",
            summary="Strong knowledge matters, but calm strategy and stress management are just as important.",
            content="""Exam performance is not just a test of knowledge. It is a test of clarity, time management, and emotional regulation under pressure.

For students, understanding the exam specification and command words is essential. Knowing whether a question asks you to describe, explain, or evaluate changes how marks are awarded. Practising this deliberately improves confidence and accuracy.

Timed practice helps normalise exam conditions. Students who practise under realistic time limits are less likely to panic and more likely to structure their answers clearly.

Stress management is part of preparation, not an afterthought. Simple techniques such as breaking questions into smaller steps, answering familiar questions first, and using steady breathing can reduce overwhelm.

For parents, support often means helping students plan revision realistically, encouraging breaks, and reinforcing that one exam does not define a person’s future.

Exam success comes from preparation that supports both the mind and wellbeing. When students feel supported rather than pressured, performance improves."""
        )

        db.session.commit()
        print("Blog content updated successfully")


if __name__ == "__main__":
    main()
