from .views import PostView
from .models import Post
last_posts = Post.objects.all().order_by('-id')[:6]

def view_all(request):
	context = {
	'last_posts':last_posts,
	}
	return context