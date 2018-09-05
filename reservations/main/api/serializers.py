from rest_framework import serializers

from ..models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'user',
            'title',
            'number_of_tables',
            'open_time',
            'close_time',
        )
