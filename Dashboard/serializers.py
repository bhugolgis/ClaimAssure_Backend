from rest_framework import serializers


class DashboardAPISerailizer(serializers.Serializer):
    CHOICES =( 
        ("Today", "Today"), 
        ("Last 7 Days", "Last 7 Days"), 
        ("Last 30 Days", "Last 30 Days"), 
        ("Last 90 Days", "Last 90 Days"), 
        ("All" , "All") 
    )
    Choice = serializers.ChoiceField(choices=CHOICES , required = False)