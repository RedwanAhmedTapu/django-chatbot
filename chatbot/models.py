from django.db import models

class ChatMessage(models.Model):
    user_message = models.TextField()  # Stores user's message
    bot_response = models.TextField()  # Stores bot's response
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"