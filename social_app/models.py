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
    def followers_count(self):
        return self.user.followers_set.count()

    def following_count(self):
        return self.user.following_set.count()

    def is_followed_by(self, user):
        """Check if given user follows this profile's user."""
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(follower=user, following=self.user).exists()
    
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
# FOLLOW MODEL
# ─────────────────────────────────────────────────────────
class Follow(models.Model):
    """
    User A follows User B.
    A = follower (who follows)
    B = following (being followed)
    """
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following_set'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

    # ─────────────────────────────────────────────────────────
# NOTIFICATION MODEL
# ─────────────────────────────────────────────────────────
class Notification(models.Model):
    """
    Notifications for like, comment, follow events.
    """
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username} ({self.notification_type})"

    def get_message(self):
        if self.notification_type == 'like':
            return f"{self.sender.username} liked your post"
        elif self.notification_type == 'comment':
            return f"{self.sender.username} commented on your post"
        elif self.notification_type == 'follow':
            return f"{self.sender.username} started following you"
        return "New notification"

    def get_icon(self):
        if self.notification_type == 'like':
            return 'bi-heart-fill'
        elif self.notification_type == 'comment':
            return 'bi-chat-fill'
        elif self.notification_type == 'follow':
            return 'bi-person-plus-fill'
        return 'bi-bell'

    def get_color(self):
        if self.notification_type == 'like':
            return 'text-danger'
        elif self.notification_type == 'comment':
            return 'text-primary'
        elif self.notification_type == 'follow':
            return 'text-success'
        return 'text-secondary'


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