

# utilsden al components.py a taşı
def GetWidgetValue(widgets, mins=None, maxs=None, defaults=None, decimal=1):
    """
    """
    if mins is None:
        mins = [0] * len(widgets)
        
    if maxs is None:
        maxs = [float('inf')] * len(widgets)

    if defaults is None:
        defaults = [0] * len(widgets)
    
    try:
        values = []
        for widget, min, max, default in zip(widgets, mins, maxs, defaults):
            values.append(int(widget.text()) if min <= int(widget.text()) <= max else default)
        
        return values[0] if len(values) == 1 else values

    except:
        return defaults[0] if len(defaults) == 1 else defaults 

