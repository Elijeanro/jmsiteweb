from django.contrib import admin

from .models import Program, ProgramContentFile, ProgramContentSchedule, ProgramContentScheduleList


class ProgramContentFileInline(admin.TabularInline):
    model = ProgramContentFile
    extra = 0


class ProgramContentScheduleListInline(admin.TabularInline):
    model = ProgramContentScheduleList
    extra = 0


class ProgramContentScheduleInline(admin.StackedInline):
    model = ProgramContentSchedule
    extra = 0
    show_change_link = True


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    inlines = [ProgramContentFileInline, ProgramContentScheduleInline]


@admin.register(ProgramContentSchedule)
class ProgramContentScheduleAdmin(admin.ModelAdmin):
    list_display = ('program', 'start_date', 'end_date', 'subtitle')
    list_filter = ('program', 'start_date')
    search_fields = ('subtitle',)
    inlines = [ProgramContentScheduleListInline]


@admin.register(ProgramContentFile)
class ProgramContentFileAdmin(admin.ModelAdmin):
    list_display = ('program', 'label', 'end_date')
    list_filter = ('program',)
    search_fields = ('label',)


@admin.register(ProgramContentScheduleList)
class ProgramContentScheduleListAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'start_time', 'end_time')
    list_filter = ('schedule',)
    search_fields = ('description',)
