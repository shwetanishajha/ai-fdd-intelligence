from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


def format_value(key: str, value) -> str:
    """Format report values for executive readability."""

    key_lower = key.lower()

    if value is None:
        return ""

    if isinstance(value, bool):
        return str(value)

    if isinstance(value, (int, float)):

        # Monetary values
        if any(term in key_lower for term in [
            "revenue",
            "ebitda",
            "working_capital",
            "change",
        ]):
            if abs(value) >= 1_000_000:
                return f"£{value / 1_000_000:.2f} million"
            return f"£{value:,.0f}"

        # Percentages
        if any(term in key_lower for term in [
            "growth",
            "margin",
            "percentage",
            "concentration",
        ]):
            return f"{value:.1f}%"

        # Generic numbers
        return f"{value:,.1f}"

    return str(value)


def add_dict_content(story, content, styles):
    """Render dictionary content cleanly."""

    for key, value in content.items():

        if key == "evidence":
            continue

        label = key.replace("_", " ").title()

        if isinstance(value, dict):
            story.append(
                Paragraph(f"<b>{label}</b>", styles["Heading2"])
            )
            add_dict_content(story, value, styles)

        elif isinstance(value, list):

            story.append(
                Paragraph(f"<b>{label}:</b>", styles["BodyText"])
            )

            for item in value:
                if isinstance(item, dict):
                    add_dict_content(story, item, styles)
                else:
                    story.append(
                        Paragraph(
                            f"• {item}",
                            styles["BodyText"],
                        )
                    )

        else:
            formatted = format_value(key, value)

            story.append(
                Paragraph(
                    f"<b>{label}:</b> {formatted}",
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 6))


def generate_fdd_pdf(report: dict, output_path: str) -> str:

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    def add_section(title: str, content):

        story.append(
            Paragraph(title, styles["Heading1"])
        )
        story.append(Spacer(1, 10))

        if isinstance(content, dict):
            add_dict_content(
                story,
                content,
                styles,
            )

        elif isinstance(content, list):

            for item in content:

                if isinstance(item, dict):
                    add_dict_content(
                        story,
                        item,
                        styles,
                    )

                else:
                    story.append(
                        Paragraph(
                            f"• {item}",
                            styles["BodyText"],
                        )
                    )

                story.append(Spacer(1, 6))

        else:
            story.append(
                Paragraph(
                    str(content),
                    styles["BodyText"],
                )
            )

        story.append(PageBreak())

    sections = [
        ("Executive Summary", report["executive_summary"]),
        ("Company Overview", report["company_overview"]),
        ("Revenue Analysis", report["revenue_analysis"]),
        ("EBITDA Analysis", report["ebitda_analysis"]),
        ("Working Capital Analysis", report["working_capital_analysis"]),
        ("Customer Concentration", report["customer_concentration"]),
        ("Financial Anomalies", report["financial_anomalies"]),
    ]

    for title, content in sections:
        add_section(title, content)

    # Key Risks
    story.append(
        Paragraph("Key Risks", styles["Heading1"])
    )
    story.append(Spacer(1, 10))

    for risk in report["key_risks"]:

        story.append(
            Paragraph(
                f"<b>{risk['risk']}</b>",
                styles["BodyText"],
            )
        )

        for evidence in risk["evidence"]:

            story.append(
                Paragraph(
                    f"Evidence: {evidence.get('text', '')}",
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Further Diligence
    story.append(
        Paragraph(
            "Further Diligence",
            styles["Heading1"],
        )
    )
    story.append(Spacer(1, 10))

    diligence = report["further_diligence"]

    if isinstance(diligence, dict):

        areas = diligence.get("areas", [])

        for area in areas:
            story.append(
                Paragraph(
                    f"• {area}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 6))

    elif isinstance(diligence, list):

        for item in diligence:
            story.append(
                Paragraph(
                    f"• {item}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Evidence Register
    story.append(
        Paragraph(
            "Evidence Register",
            styles["Heading1"],
        )
    )
    story.append(Spacer(1, 10))

    for evidence in report["evidence_register"]:

        story.append(
            Paragraph(
                f"<b>Source:</b> {evidence.get('source', '')}<br/>"
                f"<b>Page:</b> {evidence.get('page', '')}<br/>"
                f"<b>Evidence:</b> {evidence.get('text', '')}",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 10))

    doc.build(story)

    return str(path)