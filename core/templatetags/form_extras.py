from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={**(field.field.widget.attrs or {}), "class": css})


@register.filter(name="startswith")
def startswith(value, prefix):
    try:
        return str(value).startswith(str(prefix))
    except Exception:
        return False


@register.filter(name="rgba")
def rgba(hex_color, opacity_percent):
    try:
        color = str(hex_color or "").lstrip("#")
        if len(color) == 3:
            color = "".join([c * 2 for c in color])
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        a = max(0.0, min(1.0, float(opacity_percent or 0) / 100.0))
        return f"rgba({r}, {g}, {b}, {a})"
    except Exception:
        return "rgba(0,0,0,0.4)"


