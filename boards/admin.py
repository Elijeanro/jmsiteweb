from django.contrib import admin
from .models import Board, BoardType, Member, MemberPosition, Mandate, BoardMembership

class MandateInline(admin.TabularInline):
    model = Mandate
    extra = 1
    readonly_fields = ('is_current',)
    classes = ['collapse']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'parish', 'is_active', 'phone', 'email')
    list_filter = ('position', 'parish', 'is_active', 'gender')
    search_fields = ('first_name', 'last_name', 'position__name', 'parish__name')
    inlines = [MandateInline]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Nom complet'

@admin.register(MemberPosition)
class MemberPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ('member', 'start_date', 'end_date', 'is_current', 'board_type')
    list_filter = ('is_current', 'board_type', 'start_date', 'end_date')
    search_fields = ('member__first_name', 'member__last_name', 'description')
    date_hierarchy = 'start_date'
    raw_id_fields = ('member',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            if 'board_type' in request.GET:
                board_type = request.GET['board_type']
                if board_type == 'diocesan':
                    kwargs["queryset"] = Member.objects.exclude(
                        mandates__is_current=True,
                        mandates__board_type__in=['decanal', 'parish']
                    )
                elif board_type == 'parish':
                    kwargs["queryset"] = Member.objects.exclude(
                        mandates__is_current=True,
                        mandates__board_type='diocesan'
                    )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_board_type_display', 'doyenne', 'parish', 'start_date', 'end_date', 'is_current')
    list_filter = ('board_type', 'doyenne', 'parish', 'is_current')
    search_fields = ('name', 'doyenne__name', 'parish__name')
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('name', 'board_type', 'is_current')
        }),
        ('Affiliation', {
            'fields': ('doyenne', 'parish'),
            'description': 'À remplir seulement pour les bureaux décanaux et paroissiaux'
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date'),
        }),
    )

@admin.register(BoardMembership)
class BoardMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'board', 'position', 'mandate_start', 'mandate_end', 'is_active')
    list_filter = ('board__board_type', 'board', 'position', 'mandate__is_current')
    search_fields = ('member__first_name', 'member__last_name', 'position__name')
    raw_id_fields = ('member', 'board', 'position', 'mandate')

    def mandate_start(self, obj):
        return obj.mandate.start_date if obj.mandate else None
    mandate_start.short_description = 'Début mandat'

    def mandate_end(self, obj):
        return obj.mandate.end_date if obj.mandate else None
    mandate_end.short_description = 'Fin mandat'

    def is_active(self, obj):
        return obj.mandate.is_current if obj.mandate else False
    is_active.short_description = 'Actif'
    is_active.boolean = True
