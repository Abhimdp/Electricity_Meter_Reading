from django.contrib import admin
from django import forms
from .models import MeterReading

class MeterReadingAdminForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = '__all__'
        widgets = {
            'rejection_reason': forms.Select(choices=MeterReading.REJECTION_REASONS),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')

        if status == 'rejected' and not rejection_reason:
            self.add_error('rejection_reason', 'Please provide a rejection reason if the status is rejected.')

        return cleaned_data

class RejectReasonForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    rejection_reason = forms.ChoiceField(choices=MeterReading.REJECTION_REASONS, label='Rejection reason')

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    form = MeterReadingAdminForm
    list_display = ('staff_id', 'quarter_no', 'current_reading', 'electricity_units', 'uploaded_at', 'status', 'rejection_reason')
    readonly_fields = ('previous_reading', 'current_reading', 'electricity_units', 'meter_image', 'uploaded_at')
    list_filter = ('status',)
    search_fields = ('staff_id', 'quarter_no')
    actions = ['approve_reading', 'reject_reading']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'approved':
            return self.readonly_fields + ('status', 'rejection_reason')
        return self.readonly_fields

    def previous_reading(self, obj):
        previous = MeterReading.objects.filter(staff_id=obj.staff_id, quarter_no=obj.quarter_no).exclude(id=obj.id).order_by('-uploaded_at').first()
        return previous.current_reading if previous else 'N/A'
    
    previous_reading.short_description = 'Previous Reading'

    def approve_reading(self, request, queryset):
        queryset.update(status='approved', rejection_reason='')
        self.message_user(request, "Selected meter readings have been approved.")

    approve_reading.short_description = "Approve selected meter readings"

    def reject_reading(self, request, queryset):
        form = RejectReasonForm(request.POST)
        if form.is_valid():
            rejection_reason = form.cleaned_data.get('rejection_reason')
            queryset.update(status='rejected', rejection_reason=rejection_reason)
            self.message_user(request, "Selected meter readings have been rejected.")
        else:
            self.message_user(request, "Rejection reason is required to reject meter readings.", level='error')

    reject_reading.short_description = "Reject selected meter readings"

    def changelist_view(self, request, extra_context=None):
        if 'apply' in request.POST:
            action = request.POST['action']
            if action == 'reject_reading':
                form = RejectReasonForm(request.POST)
                if form.is_valid():
                    rejection_reason = form.cleaned_data.get('rejection_reason')
                    queryset = self.get_queryset(request).filter(id__in=request.POST.getlist('_selected_action'))
                    self.reject_reading(request, queryset)
                else:
                    self.message_user(request, "Rejection reason is required.", level='error')
        return super().changelist_view(request, extra_context=extra_context)

    def get_changelist_form(self, request, **kwargs):
        if request.POST.get('action') == 'reject_reading':
            return RejectReasonForm
        return super().get_changelist_form(request, **kwargs)
