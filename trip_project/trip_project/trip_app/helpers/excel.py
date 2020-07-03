import datetime
import io

# import xlsxwriter
from django.core.exceptions import ObjectDoesNotExist
from django.forms.utils import pretty_name

# HEADER_STYLE = {"bold": True}
# DEFAULT_STYLE = {}
# CELL_STYLE_MAP = (
#     (datetime.date, {"num_format": "dd/mm/yy"}),
#     (datetime.time, {"num_format": "hh:mm"}),
# )


def worldline_pretty_name(val):
    all_caps_strings = ["mid", "tid", "msf", "rrn", "mcc"]
    if str(val).lower() in all_caps_strings:
        return str(val).upper()
    elif str(val).lower() == "pmid":
        return "Parent MID"
    elif str(val).lower() == "merchant_dba_name":
        return "Merchant DBA Name"
    else:
        return pretty_name(val).title()


# def multi_getattr(obj, attr, default=None):
#     attributes = attr.split(".")
#     for i in attributes:
#         try:
#             obj = getattr(obj, i)
#         except AttributeError:
#             if default:
#                 return default
#             else:
#                 raise
#     return obj


# def get_column_head(obj, name):
#     name = name.rsplit(".", 1)[-1]
#     return worldline_pretty_name(name)


# def get_column_cell(obj, name):
#     try:
#         attr = multi_getattr(obj, name)
#     except ObjectDoesNotExist:
#         return None
#     if hasattr(attr, "_meta"):
#         # A Django Model (related object)
#         return unicode(attr).strip()  # noqa: F821
#     elif hasattr(attr, "all"):
#         # A Django queryset (ManyRelatedManager)
#         return ", ".join(unicode(x).strip() for x in attr.all())  # noqa: F821
#     return attr


# def queryset_to_workbook(
#     queryset, columns, header_style=None, default_style=None, cell_style_map=None
# ):
#     output = io.BytesIO()
#     workbook = xlsxwriter.Workbook(output)
#     worksheet = workbook.add_worksheet("Report")
#     cell_format_map = {}
#     if not header_style:
#         header_style = HEADER_STYLE

#     if not default_style:
#         default_style = DEFAULT_STYLE
#     if not cell_style_map:
#         cell_style_map = CELL_STYLE_MAP

#     header_format = workbook.add_format(header_style)
#     default_cell_format = workbook.add_format(default_style)
#     for cell_type, cell_style in cell_style_map:
#         cell_format_map[cell_type] = workbook.add_format(cell_style)

#     obj = queryset.first()
#     for y, column in enumerate(columns):
#         value = get_column_head(obj, column)
#         worksheet.write(0, y, value, header_format)

#     for x, obj in enumerate(queryset, start=1):
#         for y, column in enumerate(columns):
#             value = get_column_cell(obj, column)
#             style = default_cell_format
#             for value_type, cell_format in cell_format_map.items():
#                 if isinstance(value, value_type):
#                     style = cell_format
#             worksheet.write(x, y, value, style)

#     workbook.close()
#     output.seek(0)
#     return output
