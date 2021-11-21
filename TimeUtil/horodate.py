from datetime import datetime


def horadate(format_type="standard"):

    str_format = ""

    if format_type == "standard":
        str_format=datetime.now().strftime("%d%m%Y_%H%M%S")
    elif format_type == "mensuel":
        str_format = datetime.now().strftime("%d%m%Y")
    elif format_type=="horaire":
        str_format = datetime.now().strftime("%H%M%S")
    elif format_type == "americain":
        str_format=datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        str_format=datetime.now().strftime("%H%M%S")

    return str_format


def convert_time( milliseconds):
    seconds = (int)(milliseconds / 1000) % 60
    minutes = (int)((milliseconds / (1000 * 60)) % 60)
    hours = (int)((milliseconds / (1000 * 60 * 60)) % 24)
    model = "{0:02}:{1:02}:{2:02}"
    model = model.format(hours, minutes, seconds)
    return model