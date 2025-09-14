from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator

class ReportTemplate(models.Model):
    """Templates for different types of reports"""
    REPORT_TYPE_CHOICES = [
        ('sales', 'Sales Report'),
        ('purchases', 'Purchase Report'),
        ('inventory', 'Inventory Report'),
        ('expenses', 'Expense Report'),
        ('profit_loss', 'Profit & Loss Report'),
        ('customer_statement', 'Customer Statement'),
        ('supplier_statement', 'Supplier Statement'),
        ('aging', 'Aging Report'),
        ('stock_movement', 'Stock Movement Report'),
        ('low_stock', 'Low Stock Report'),
        ('installment', 'Installment Report'),
        ('daily_summary', 'Daily Summary'),
        ('weekly_summary', 'Weekly Summary'),
        ('monthly_summary', 'Monthly Summary'),
        ('custom', 'Custom Report'),
    ]
    
    FREQUENCY_CHOICES = [
        ('once', 'One Time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    
    # Report Configuration
    parameters = models.JSONField(default=dict, blank=True)  # Store report parameters as JSON
    filters = models.JSONField(default=dict, blank=True)     # Store filters as JSON
    columns = models.JSONField(default=list, blank=True)     # Store selected columns
    
    # Scheduling
    is_scheduled = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='once')
    schedule_time = models.TimeField(blank=True, null=True)
    next_run_date = models.DateTimeField(blank=True, null=True)
    last_run_date = models.DateTimeField(blank=True, null=True)
    
    # Output Settings
    output_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    auto_email = models.BooleanField(default=False)
    email_recipients = models.TextField(blank=True, help_text="Comma-separated email addresses")
    email_subject = models.CharField(max_length=200, blank=True)
    email_body = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='created_report_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"
    
    class Meta:
        db_table = 'report_templates'
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'
        ordering = ['report_type', 'name']

class GeneratedReport(models.Model):
    """Records of generated reports"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='generated_reports', blank=True, null=True)
    report_name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=ReportTemplate.REPORT_TYPE_CHOICES)
    
    # Generation Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField(default=dict, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # File Information
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(default=0)
    file_format = models.CharField(max_length=10, choices=ReportTemplate.FORMAT_CHOICES, default='pdf')
    
    # Date Range
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    
    # Generation Statistics
    total_records = models.IntegerField(default=0)
    generation_time = models.FloatField(default=0.0)  # Time taken in seconds
    error_message = models.TextField(blank=True)
    
    # Email Details
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(blank=True, null=True)
    email_recipients = models.TextField(blank=True)
    
    # Tracking
    generated_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True)
    downloaded_at = models.DateTimeField(blank=True, null=True)
    download_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.report_name} - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2) if self.file_size > 0 else 0
    
    class Meta:
        db_table = 'generated_reports'
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'
        ordering = ['-generated_at']

class ReportSubscription(models.Model):
    """User subscriptions to scheduled reports"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='report_subscriptions')
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='subscriptions')
    
    # Subscription Settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    custom_parameters = models.JSONField(default=dict, blank=True)
    custom_filters = models.JSONField(default=dict, blank=True)
    
    # Email Settings
    email_address = models.EmailField(validators=[EmailValidator()])
    send_email = models.BooleanField(default=True)
    email_format = models.CharField(max_length=10, choices=ReportTemplate.FORMAT_CHOICES, default='pdf')
    
    # Tracking
    subscribed_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)
    total_reports_sent = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.template.name}"
    
    class Meta:
        db_table = 'report_subscriptions'
        verbose_name = 'Report Subscription'
        verbose_name_plural = 'Report Subscriptions'
        unique_together = ['user', 'template']
        ordering = ['-subscribed_at']

class ReportCategory(models.Model):
    """Categories for organizing reports"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'report_categories'
        verbose_name = 'Report Category'
        verbose_name_plural = 'Report Categories'
        ordering = ['sort_order', 'name']

class ReportAccess(models.Model):
    """Control access to specific reports by user roles"""
    report_type = models.CharField(max_length=30, choices=ReportTemplate.REPORT_TYPE_CHOICES)
    user_role = models.CharField(max_length=20)  # Should match User.ROLE_CHOICES
    can_view = models.BooleanField(default=True)
    can_generate = models.BooleanField(default=True)
    can_schedule = models.BooleanField(default=False)
    can_export = models.BooleanField(default=True)
    can_email = models.BooleanField(default=False)
    
    # Data Access Restrictions
    data_filters = models.JSONField(default=dict, blank=True)  # Additional filters based on role
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user_role} - {self.get_report_type_display()}"
    
    class Meta:
        db_table = 'report_access'
        verbose_name = 'Report Access'
        verbose_name_plural = 'Report Access'
        unique_together = ['report_type', 'user_role']
        ordering = ['report_type', 'user_role']

class DashboardWidget(models.Model):
    """Dashboard widgets for displaying key metrics"""
    WIDGET_TYPE_CHOICES = [
        ('chart', 'Chart'),
        ('kpi', 'KPI Card'),
        ('table', 'Data Table'),
        ('gauge', 'Gauge'),
        ('progress', 'Progress Bar'),
        ('alert', 'Alert Box'),
    ]
    
    CHART_TYPE_CHOICES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small (1x1)'),
        ('medium', 'Medium (2x1)'),
        ('large', 'Large (2x2)'),
        ('wide', 'Wide (3x1)'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPE_CHOICES, blank=True)
    
    # Data Configuration
    data_source = models.CharField(max_length=100)  # Model or view name
    data_query = models.JSONField(default=dict, blank=True)  # Query parameters
    refresh_interval = models.IntegerField(default=300)  # Seconds
    
    # Display Settings
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium')
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#333333')
    
    # Access Control
    allowed_roles = models.JSONField(default=list, blank=True)  # List of roles that can see this widget
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"
    
    class Meta:
        db_table = 'dashboard_widgets'
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
        ordering = ['position_y', 'position_x']

class AnalyticsEvent(models.Model):
    """Track user analytics and system events"""
    EVENT_TYPE_CHOICES = [
        ('page_view', 'Page View'),
        ('report_generated', 'Report Generated'),
        ('report_downloaded', 'Report Downloaded'),
        ('search', 'Search'),
        ('filter_applied', 'Filter Applied'),
        ('export', 'Data Export'),
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('error', 'System Error'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='analytics_events', blank=True, null=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    page_url = models.CharField(max_length=500, blank=True)
    event_data = models.JSONField(default=dict, blank=True)  # Additional event data
    
    # Browser/Session Info
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(blank=True, null=True)  # For events that have duration
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{user_str} - {self.get_event_type_display()} at {self.timestamp}"
    
    class Meta:
        db_table = 'analytics_events'
        verbose_name = 'Analytics Event'
        verbose_name_plural = 'Analytics Events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
        ]