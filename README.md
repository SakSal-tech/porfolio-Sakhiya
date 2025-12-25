# Sakhiya Salad – Portfolio

This repository contains the source code for my personal software engineering portfolio.

The site showcases my background, skills, projects, and writing, with a focus on clean design, clarity, and thoughtful engineering. It is built to be lightweight, readable, and easy to extend as my work evolves.

---

## 🌐 Live Site

(Add  deployed URL here)

---

## Features

## Features

- Responsive, modern layout across desktop and mobile devices
- Animated hero section with a typewriter-style code/output effect
- Database-backed blog with publish and update capabilities
- Contact form with backend handling, validation, and persistence
- Tutoring booking system with server-side validation
- Dark mode and high-contrast theme support
- Accessibility-focused design using semantic HTML
- Keyboard navigation support and visible focus states
- Reduced-motion support respecting user system preferences
- Accessible colour contrast across themes (light, dark, high contrast)
- ARIA labels and screen-reader-friendly form feedback
- Smooth scrolling and subtle animations with motion-safe fallbacks


---

## Technologies & Tools Used

### Frontend

- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5

### Styling & UX

- CSS Grid and Flexbox
- Custom CSS variables
- Typewriter animation with custom cursor
- Intersection Observer API

### Backend

- Python
- Flask
- Jinja2

---

## Project Motivation & Architecture
### Why Python Flask and Jinja with JS, HTML & CSS/Bootstrap?

This portfolio was intentionally built as a dynamic web application using Flask, Jinja2, and Bootstrap alongside HTML, CSS, and JavaScript. Rather than a purely static site, the goal was to create a foundation capable of supporting real interaction and long-term growth, including database-backed blog publishing, contact and booking workflows, and an administrative interface for content management. While I considered building this project using Java Spring Boot with a React and TypeScript frontend (a stack I am familiar with), I chose Flask and Jinja2 to keep the architecture lightweight, transparent, and tightly integrated, allowing a stronger focus on clarity, maintainability, and server-rendered content.

Although Bootstrap is used selectively for layout structure and responsiveness, the majority of the visual design is implemented through custom-written CSS. This provides full control over typography, spacing, color systems, and component behavior, including improved accessibility and a dark mode theme. Flask handles routing, server-side logic, and database integration, while Jinja2 enables reusable templates and dynamic content rendering. Together, this stack allows the portfolio to function not only as a showcase, but as a complete, maintainable web application that reflects my approach to real-world software engineering.


## Design Principles

- Clarity over cleverness
- Separation of concerns
- Lightweight and maintainable code
- User-focused design

---

## Project Structure

```
.
├── app.py
├── templates/
│   ├── index.html
│   └── blog.html
├── static/
│   ├── styles.css
│   └── assets/
└── README.md
```

---

## Running Locally

```bash
git clone https://github.com/my-username/portfolio.git
cd portfolio
pip install flask
python app.py
```

Visit: http://127.0.0.1:5000

---

## Future Improvements

- Admin dashboard for managing blog posts, messages, and bookings
- Enhanced form validation and error handling
- Performance optimizations and caching (Blogs)
- Add automated tests for backend routes

---

## Copyright

© 2025 Sakhiya Salad. All rights reserved.

This is a personal portfolio. The project and its contents are provided for viewing purposes only.
No permission is granted to copy, modify, or redistribute this code or design.


© 2025 Sakhiya Salad. All rights reserved.

---

## Contact

- GitHub: https://github.com/SakSal-tech
- LinkedIn: https://www.linkedin.com/in/sakhiya-salad
