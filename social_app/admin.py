from django.contrib import admin
from .models import Profile, Post, Like, Comment


# ─────────────────────────────────────────────────────────
# PROFILE ADMIN
# ─────────────────────────────────────────────────────────
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)


# ─────────────────────────────────────────────────────────
# POST ADMIN
# ─────────────────────────────────────────────────────────
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'media_type', 'caption_short', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'caption')
    readonly_fields = ('created_at',)

    def media_type(self, obj):
        """Post-la enna media type irukku-nu show pannum."""
        if obj.image:
            return '🖼️ Image'
        elif obj.youtube_video_id:
            return '▶️ YouTube'
        elif obj.instagram_url:
            return '📸 Instagram'
        return '❌ Empty'
    media_type.short_description = 'Type'

    def caption_short(self, obj):
        """Caption first 40 chars mattum."""
        return obj.caption[:40] + '...' if len(obj.caption) > 40 else obj.caption
    caption_short.short_description = 'Caption'


# ─────────────────────────────────────────────────────────
# LIKE ADMIN
# ─────────────────────────────────────────────────────────
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


# ─────────────────────────────────────────────────────────
# COMMENT ADMIN
# ─────────────────────────────────────────────────────────
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text_short', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'text')

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Comment'