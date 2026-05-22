from django.db import models
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
# from location_field.models.plain import PlainLocationField
# from django.contrib.gis.db import models
PRIVACY_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
    )
JOIN_CHOICES = (
    ('anyone', 'automatic join'),
    ('only_approved', 'approval to join'),
)
POST_CHOICES = (
    ('members', 'all members'),
    ('admin_only', 'only admin'),
)

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='GroupMembership', related_name='group')
    join_privacy = models.CharField(max_length=50, choices=JOIN_CHOICES, default='anyone')
    who_can_post =models.CharField(max_length=20, choices=POST_CHOICES, default='members')
    # parent_group = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subgroups')

    def __str__(self):
        return self.name

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    def is_admin(self, user):
        return self.members.filter(user=user, role='admin').exists()

class GroupMembership(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"
    def is_admin(self):
        return self.role == 'admin'

class GroupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='requests')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    text =models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"Request by {self.user.username} to join {self.group.name}"

class GroupCreationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    join_privacy = models.CharField(max_length=50, choices=JOIN_CHOICES, default='anyone')
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    who_can_post =models.CharField(max_length=20, choices=POST_CHOICES, default='members')

    def __str__(self):
        return f"Request by {self.user.username} for {self.group_name}"

class Location(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    # location_field= models.PointField()
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip}"


class Event(models.Model):
    EVENT_LOCATION_CHOICES = [
        ('remote', 'Remote'),
        ('in_person', 'In Person'),
    ]
    EVENT_TYPE_CHOICES = [
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('meetup', 'Meetup'),
        ('bible study', 'Bible Study')
    ]
    title = models.CharField(max_length=150)
    description = HTMLField()
    group= models.ForeignKey(Group,on_delete=models.SET_NULL, null=True, related_name='events')
    event_date = models.DateTimeField()
    location_type = models.CharField(max_length=50, choices=EVENT_LOCATION_CHOICES, default='remote')
    # location_details = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    # attendees = models.ManyToManyField(User, related_name='event_attendees',blank=True)
    # max_attendees = models.PositiveIntegerField(default=0)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    # registration_required = models.BooleanField(default=False)
    # registration_deadline = models.DateField(null=True, blank=True)
    # cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # duration = models.DurationField(null=True, blank=True)
    # is_recurring = models.BooleanField(default=False)
    # recurrence_pattern = models.CharField(max_length=20, blank=True, null=True)
    # accessibility_options = models.TextField(blank=True)


class ChurchCreationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    join_privacy = models.CharField(max_length=50, choices=JOIN_CHOICES, default='anyone')
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    who_can_post =models.CharField(max_length=20, choices=POST_CHOICES, default='members')

    def __str__(self):
        return f"Request by {self.user.username} for {self.group_name}"

class ChurchGroup(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    description = models.TextField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='ChurchMembership', related_name='church_group')
    join_privacy = models.CharField(max_length=50, choices=JOIN_CHOICES, default='anyone')
    who_can_post =models.CharField(max_length=20, choices=POST_CHOICES, default='members')
    parent_group = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='smallgroups')

    def __str__(self):
        return self.name

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    def is_admin(self, user):
        return self.members.filter(user=user, role='admin').exists()

class ChurchMemberRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChurchGroup, on_delete=models.CASCADE, related_name='requests_church')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    text = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"Request by {self.user.username} to join {self.group.name}"

class ChurchMembership(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChurchGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"
    def is_admin(self):
        return self.role == 'admin'





