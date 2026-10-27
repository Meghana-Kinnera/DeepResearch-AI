from fpdf import FPDF

def convert_markdown_to_pdf(text: str) -> bytes:
    """
    Converts markdown report text into a clean, formatted PDF document byte stream safely.
    Always resets X cursor position before multi_cell calls to prevent fpdf horizontal space exceptions.
    Guaranteed to return valid PDF bytes.
    """
    if not text:
        text = "# Deep Research Report\n\nNo report content available."
        
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=10)
        
        # Clean unicode symbols, quotes, em-dashes, and box-drawing characters
        cleaned_text = (
            text.replace("—", "-")
                .replace("“", '"')
                .replace("”", '"')
                .replace("‘", "'")
                .replace("’", "'")
                .replace("•", "*")
                .replace("…", "...")
                .replace("➔", "->")
                .replace("│", "|")
                .replace("─", "-")
                .replace("┌", "+")
                .replace("┐", "+")
                .replace("└", "+")
                .replace("┘", "+")
                .replace("├", "+")
                .replace("┤", "+")
                .replace("┬", "+")
                .replace("┴", "+")
                .replace("┼", "+")
                .replace("▲", "^")
                .replace("▼", "v")
                .replace("◄", "<")
                .replace("►", ">")
        )
        
        lines = cleaned_text.splitlines()
        for line in lines:
            # Crucial: Always reset X cursor to left margin to avoid right-edge overflow
            pdf.set_x(pdf.l_margin)
            
            line_str = line.strip()
            if not line_str:
                pdf.ln(3)
                continue
                
            safe_ascii = line_str.encode("ascii", "replace").decode("ascii")
            
            if line_str.startswith("# "):
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 14)
                pdf.multi_cell(0, 8, safe_ascii[2:])
                pdf.ln(1)
            elif line_str.startswith("## "):
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 12)
                pdf.multi_cell(0, 7, safe_ascii[3:])
                pdf.ln(1)
            elif line_str.startswith("### "):
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 6, safe_ascii[4:])
            else:
                pdf.set_font("Helvetica", size=10)
                # Break long unbroken words/URLs exceeding 40 chars
                words = safe_ascii.split(" ")
                safe_words = []
                for w in words:
                    if len(w) > 40:
                        chunks = [w[i:i+35] for i in range(0, len(w), 35)]
                        safe_words.append(" ".join(chunks))
                    else:
                        safe_words.append(w)
                safe_line = " ".join(safe_words)
                
                pdf.multi_cell(0, 5, safe_line)
                
        return bytes(pdf.output())
    except Exception as e:
        print(f"[PDF Exporter Fallback] {e}")
        fallback_pdf = FPDF()
        fallback_pdf.add_page()
        fallback_pdf.set_font("Helvetica", size=10)
        fallback_pdf.set_x(fallback_pdf.l_margin)
        safe_fallback = text.encode("ascii", "replace").decode("ascii")[:3000]
        fallback_pdf.multi_cell(0, 5, safe_fallback)
        return bytes(fallback_pdf.output())
