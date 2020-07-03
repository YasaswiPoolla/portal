import datetime

from django.db.models import Count, Sum
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from trip_project.trip_app.helpers.excel import worldline_pretty_name


class BaseMidAuthenticatedViewset(viewsets.ModelViewSet):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user is not None and self.request.user.is_authenticated:
            
            return super(BaseMidAuthenticatedViewset, self).dispatch(request, *args, **kwargs)


class BaseFilterablePaginatedViewset(BaseMidAuthenticatedViewset):
    multi_select_filterable_columns = []
    columns_to_display = None
    columns_to_exclude = ["trip_sqn", "user"]
    columns_with_text_filter = [
        "from_location",
        "to_location",
        "trip_distance,"
    ]
    date_column = "trip_date"
    date_renamed_column = "day"
    db_date_column = "tripdate"
    date_type = "date"
    page = 1
    per_page = 10
    date_input_format = "dd-MM-yyyy HH:mm:ss"
    date_output_format = "%d-%m-%Y"


    __available_multislect_filters = ['from_location']
    serializer_columns = []
    __generated_display_columns = []
    default_start_date = (
        (datetime.datetime.now() - datetime.timedelta(days=90))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .date()
    )
    filter_only_columns = []

    def set_columns(self):
        self.set_generated_columns()
        self.set_available_multiselct_filters()
        columns_to_remove = self.get_columns_to_remove()
        self.remove_columns(columns_to_remove)

    def set_generated_columns(self):
        self.__generated_display_columns = []
        if self.columns_to_display is not None and len(self.columns_to_display) > 0:
            for column in self.columns_to_display:
                if column not in self.columns_to_exclude:
                    self.__generated_display_columns.append(column)
        else:
            for field in self.model._meta.fields:
                if field.name not in self.columns_to_exclude:
                    self.__generated_display_columns.append(field.name)

    def set_available_multiselct_filters(self):
        self.__available_multislect_filters = []
        for column in self.__generated_display_columns:
            if column in self.multi_select_filterable_columns:
                self.__available_multislect_filters.append(column)

    def get_columns_to_remove(self):
        columns_to_remove = ["trip_sqn"]
        

        return columns_to_remove

    def remove_columns(self, columns_to_remove):
        for column_to_remove in columns_to_remove:
            if column_to_remove in self.__available_multislect_filters:
                self.__available_multislect_filters.remove(column_to_remove)
            if column_to_remove in self.__generated_display_columns:
                self.__generated_display_columns.remove(column_to_remove)

    def get_queryset(self):
        queryset = self.queryset

        filters = {}
        if self.date_column:
            filters["{}__gte".format(self.date_column)] = self.default_start_date

        queryset = queryset.filter(**filters)

        return queryset

    @action(methods=["post"], detail=False, url_path="columns")
    def columns(self, request):
        self.set_columns()
        queryset = self.get_queryset()
        column_filters = request.data.get("columnFilters", {})
        choices = self.create_base_choices(column_filters, queryset)

        columns = []
        for column in self.filter_only_columns + self.__generated_display_columns:
            if column in self.columns_to_exclude:
                continue
            ui_column = {
                "label": worldline_pretty_name(column),
                "field": column,
                "filter_only": False,
            }
            if column in self.filter_only_columns:
                ui_column["filter_only"] = True
            if column == self.date_column:
                ui_column["filterOptions"] = {"enabled": True, "trigger": "enter"}
                ui_column["type"] = "date"
                ui_column["dateInputFormat"] = self.date_input_format
                ui_column["dateOutputFormat"] = "dd-MM-yyyy"
            elif column in self.__available_multislect_filters:
                ui_column["filterOptions"] = {
                    "enabled": True,
                    "filterMultiselectDropdownItems": choices[column],
                }
            elif column in self.columns_with_text_filter:
                ui_column["filterOptions"] = {"enabled": True, "trigger": "enter"}
            if column in self.serializer_columns:
                ui_column["sortable"] = False
            ui_column["thClass"] = "text-center"
            ui_column["tdClass"] = "text-center"
            columns.append(ui_column)
        return Response(columns)

    def create_base_choices(self, column_filters, queryset):
        choices = {column: set() for column in self.__available_multislect_filters}
        for column in self.__available_multislect_filters:
            column_values = queryset.order_by().values_list(column, flat=True).distinct()
            choices[column] = list(column_values)

        return choices

    @action(methods=["post"], detail=False, url_path="data")
    def data(self, request):
        queryset = self.get_queryset()
        page = request.data.get("page", self.page)
        per_page = request.data.get("perPage", self.per_page)
        column_filters = request.data.get("columnFilters", {})
        download = request.data.get("download", None)
        sort_options = request.data.get("sort", [])
        excel_fields = request.data.get("fields", None)

        queryset = self.filter_multiselect_queryset(queryset, column_filters)
        sorting = []
        for sort_option in sort_options:
            if sort_option["type"] == "asc":
                sorting.append(sort_option["field"])
            elif sort_option["type"] == "desc":
                sorting.append("-" + sort_option["field"])
        queryset = queryset.order_by(*sorting)
        count = queryset.count()

        records = queryset[per_page * (page - 1) : per_page * page]
        serializer = self.serializer_class(records, many=True)
        return Response({"rows": serializer.data, "count": count})

    def check_date_format(self, date_string):
        try:
            date = datetime.datetime.strptime(date_string, self.date_output_format).date()
            return date
        except Exception:
            return None

    def filter_multiselect_queryset(self, queryset, column_filters):
        self.set_columns()
        filter_kwargs = {}
        for filter_column, filter_value in column_filters.items():
            if filter_column in self.__available_multislect_filters and len(filter_value) > 0:
                filter_kwargs[filter_column + "__in"] = filter_value
            elif filter_column == self.date_column and filter_value.strip() != "":
                end_date, start_date = self.get_start_end_dates_from_filter(filter_value)

                if start_date and end_date:
                    filter_kwargs[filter_column + "__gte"] = start_date
                    filter_kwargs[filter_column + "__lte"] = end_date
                elif start_date:
                    filter_kwargs[filter_column] = start_date
            elif type(filter_value) == str and filter_value.strip() != "":
                filter_kwargs[filter_column + "__icontains"] = filter_value.strip()

        return queryset.filter(**filter_kwargs)

    def get_start_end_dates_from_filter(self, filter_value):
        filter_value_dates = filter_value.split(" to ")
        start_date = self.check_date_format(filter_value_dates[0])
        if start_date is None:
            start_date = self.default_start_date
        end_date = None
        if len(filter_value_dates) > 1:
            end_date = self.check_date_format(filter_value_dates[1])
            if end_date is None:
                end_date = datetime.datetime.now().date()
        if not end_date:
            end_date = start_date

        if self.date_type == "datetime":
            start_time = (
                datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).time()
            )
            end_time = (
                datetime.datetime.now()
                .replace(hour=23, minute=59, second=59, microsecond=99999)
                .time()
            )
            start_date = datetime.datetime.combine(start_date, start_time)
            end_date = datetime.datetime.combine(end_date, end_time)

        return end_date, start_date
