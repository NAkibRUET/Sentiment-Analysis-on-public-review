from django.shortcuts import render
from .models import profile
from .models import login1
from .models import comments
from django.http import JsonResponse

from textblob import TextBlob

# Create your views here.
def login(request):
	if request.method == "GET":
		return render(request, 'login.html')
	if request.method == "POST":
		ruse = request.POST.get('use')

		rpass = request.POST.get('pass')
		print(ruse)
		check = login1.objects.filter(username=ruse, password=rpass)
		if len(check)!=0:
			var = 1
			request.session['wow']=request.POST['use'];
		else:
			var = 0
		dic={
			'varr':var,
			#'bal':check
		}	
		return JsonResponse(dic)
		#return render(request, 'login.html',context=dic)
	

def adminpanel(request):
	if request.method=="GET":
		if 'wow' in request.session:
			commentcontent = comments.objects.all().order_by('id').reverse() 
			allcontent=profile.objects.all().order_by('id').reverse()
			makedictionary={
				'userinfo':allcontent,
				'comments':commentcontent,
			}
			return render(request, 'index.html',context=makedictionary)
		else:
			return render(request, 'login.html')
	if request.method=="POST":
		rtitle=request.POST.get('title')
		rimage=request.FILES['image']
		sql=profile(title=rtitle, image=rimage)
		sql.save()
		allcontent=profile.objects.all().order_by('id').reverse()
		makedictionary={
			'userinfo':allcontent
		}
		return render(request, 'index.html',context=makedictionary)

def logout(request):
	if request.method=="GET":
		
		return render(request,'login.html')

	if request.method=="POST":
		request.session.pop('wow')
		return render(request,'login.html')

def index(request):
	if request.method=="GET":
		commentcontent = comments.objects.all().order_by('id').reverse() 
		allcontent=profile.objects.all().order_by('id').reverse()
		makedictionary={
			'userinfo':allcontent,
			'comments':commentcontent
		}
		return render(request,'home.html',context=makedictionary)

	if request.method=="POST":
		rtitle=request.POST.get('title')
		ruser=request.POST.get('user')
		rcomment=request.POST.get('comment')
		sql=comments(user=ruser, title=rtitle, comment=rcomment)
		sql.save()
		commentcontent = comments.objects.all().order_by('id').reverse() 
		allcontent=profile.objects.all().order_by('id').reverse()
		makedictionary={
			'userinfo':allcontent,
			'comments':commentcontent
		}

		return render(request,'home.html',context=makedictionary)

def analysis(request,analysis_title):
	if request.method=="GET":
		if 'wow' in request.session:
			if 'haha' in request.session:
				var = request.session['haha']
				contents = comments.objects.filter(title=var)
				img = profile.objects.filter(title=var)
				pos_count = 0
				neg_count = 0
				total_count = 0
				per_pos = 0
				per_neg = 0
				subjectivity = 0
				for i in contents:
					analysis = TextBlob(i.comment)
					if analysis.sentiment.polarity >= 0.15:
						pos_count = pos_count + 1
						per_pos = per_pos + analysis.sentiment.polarity
					if analysis.sentiment.polarity < 0.0:
						neg_count = neg_count + 1
						per_neg = per_neg + analysis.sentiment.polarity 
					total_count = total_count + 1
					subjectivity = subjectivity + analysis.sentiment.subjectivity
					
				subjectivity = (subjectivity / total_count)*100
				per_pos = (per_pos / pos_count)*100
				per_neg = (per_neg / neg_count)*100
				successrate = (neg_count+pos_count)/total_count
				successrate = successrate*100

				res_neg = (neg_count / total_count)*100
				res_pos = (pos_count / total_count)*100
				makedictionary={
					'imag':img,
					'rneg':round(res_neg,2),
					'rpos':round(res_pos,2),
					'perpos':round(per_pos,2),
					'perneg':round(per_neg,2),
					'sub': round(subjectivity,2),
					'srate':round(successrate,2)
				}
				return render(request, 'analysis.html',context=makedictionary)
		else:
			return render(request, 'login.html')
	if request.method=="POST":
		if 'wow' in request.session:
			rtitle=analysis_title
			request.session['haha']=request.POST['title'];
			contents = comments.objects.filter(title=rtitle)
			img = profile.objects.filter(title=rtitle)
			pos_count = 0
			neg_count = 0
			total_count = 0
			per_pos = 0
			per_neg = 0
			subjectivity = 0
			for i in contents:
				analysis = TextBlob(i.comment)
				if analysis.sentiment.polarity >= .15:
					pos_count = pos_count + 1
					per_pos = per_pos + analysis.sentiment.polarity
				if analysis.sentiment.polarity < 0:
					per_neg = per_neg + analysis.sentiment.polarity
					neg_count = neg_count + 1 
				total_count = total_count + 1
				subjectivity = subjectivity + analysis.sentiment.subjectivity
				
			subjectivity = (subjectivity / total_count)*100
			per_pos = (per_pos / pos_count)*100
			per_neg = (per_neg / neg_count)*100
			successrate = (neg_count+pos_count)/total_count
			successrate = successrate*100
			res_neg = (neg_count / total_count)*100
			res_pos = (pos_count / total_count)*100
			makedictionary={
				'imag':img,
				'rneg':round(res_neg,2),
				'rpos':round(res_pos,2),
				'perpos':round(per_pos,2),
				'perneg':round(per_neg,2),
				'sub': round(subjectivity,2),
				'srate':round(successrate,2)
			}
			return render(request, 'analysis.html',context=makedictionary)
		else:
			return render(request, 'login.html')