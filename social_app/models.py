from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# ─────────────────────────────────────────────────────────
# PROFILE MODEL
# ─────────────────────────────────────────────────────────
class Profile(models.Model):
    """
    User-oda extra info store panna.
    Auto-create aagum when new User registers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True, default="")
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ─────────────────────────────────────────────────────────
# POST MODEL
# ─────────────────────────────────────────────────────────
class Post(models.Model):
    """
    User-oda post. 3 types:
    1. Image upload (Cloudinary)
    2. YouTube video (via search)
    3. Instagram URL (redirect)
    At least one of these must be present.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # Type 1: Image upload
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    # Type 2: YouTube video
    youtube_video_id = models.CharField(max_length=20, blank=True, null=True)
    youtube_title = models.CharField(max_length=200, blank=True, null=True)
    youtube_thumbnail = models.URLField(blank=True, null=True)
    
    # Type 3: Instagram URL
    instagram_url = models.URLField(blank=True, null=True)
    
    # Common
    caption = models.TextField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    # ─────────────────────────────────────────────────
    # VALIDATION: At least one media required
    # ─────────────────────────────────────────────────
    def clean(self):
        if not self.image and not self.youtube_video_id and not self.instagram_url:
            raise ValidationError(
                "Please upload an image, or select a YouTube video, or paste an Instagram URL."
            )

    # ─────────────────────────────────────────────────
    # HELPER METHODS (Template-la use pannuvom)
    # ─────────────────────────────────────────────────
    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def has_image(self):
        return bool(self.image)

    def is_youtube(self):
        return bool(self.youtube_video_id)

    def is_instagram(self):
        return bool(self.instagram_url)


# ─────────────────────────────────────────────────────────
# LIKE MODEL
# ─────────────────────────────────────────────────────────
class Like(models.Model):
    """
    User-oda like on a post.
    Same user same post-ku oru thadava mattum like panna mudiyum.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes Post#{self.post.id}"


# ─────────────────────────────────────────────────────────
# COMMENT MODEL
# ─────────────────────────────────────────────────────────
class Comment(models.Model):
    """User-oda comment on a post."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Oldest first

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


# ─────────────────────────────────────────────────────────
# SIGNALS: Auto-create Profile when User registers
# ─────────────────────────────────────────────────────────
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """New User create aana udane Profile create pannum."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User save aana udane Profile-um save aagum."""
    instance.profile.save()