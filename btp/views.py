from btp.models  import *
from btp.forms   import *
from btp.methods import *

from django.core.exceptions import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib.auth.views import logout
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url,render
from django.template.response import TemplateResponse
from django.core.mail import send_mail

class IndexView(TemplateView):
	template_name = 'index/index.html'
	def get_context_data(self, **kwargs):
		context=super(IndexView,self).get_context_data(**kwargs)
		context = {'title':'Cosmos'}
		
		return context
	def dispatch(self, *args, **kwargs):
		return super(IndexView,self).dispatch(*args,**kwargs)
class BTPIndexView(TemplateView):
	template_name = 'btp/btpindex.html'
			
	def post(self, request, *args, **kwargs):
		usertype = getUserTypes(self.request.user)
		if "STUDENT" in usertype:
			form = SubmissionForm(self.request.FILES, self.request.POST)
			print self.request.FILES['fileuploaded']
                	fileuploaded = self.request.FILES['fileuploaded']
			

			pg = getProjectGroupByStudentId(getStudentIdByUser(self.request.user))
			evalset = getBTPEvalSetByProjectGroup(pg)
			getAllBTPProjectGroupsByEvalSet(evalset)		
			pgid = pg.id
			try:
				currweek = getCurrentWeek()
				week = BTPSetWeek.objects.get(week = currweek, sets=evalset)
				try:
					submit = BTPSubmission.objects.get(week = week , projectgroup = pg)
		
					submit.fileuploaded = fileuploaded
					submit.submitted_by = self.request.user 
					
					submit.save()
				except ObjectDoesNotExist as error:
					submit = BTPSubmission( week = week , projectgroup = pg, fileuploaded = fileuploaded, submitted_by = self.request.user )
					submit.save()
				return JsonResponse({"posted":"True"})
			except ObjectDoesNotExist as error:
				week = BTPSetWeek.objects.all()[0]
				print "Here"
		return JsonResponse({"posted":"False"})
	def get_context_data(self, **kwargs):
		context=super(BTPIndexView,self).get_context_data(**kwargs)
		
		students = BTPStudent.objects.order_by('rollno')
		faculty = Faculty.objects.order_by('user__first_name')
		
		
		context = {'title':'Home - BTP',
			   'students':students,
			   'faculty':faculty,
			   'header':'B-Tech Projects Portal',
                           'MEDIA_URL':settings.MEDIA_URL,
			   		
		}
		usertypes = getUserTypes(self.request.user)
                print usertypes
		if "STUDENT" in usertypes:
			mysubmissions = BTPSubmission.objects.filter(submitted_by = self.request.user).order_by('submitted_at')
			sets = getBTPEvalSetByProjectGroup( getProjectGroupByStudentId(getStudentIdByUser(self.request.user)) )
			week = getCurrentWeek()
			context['submissionsform']=SubmissionForm(self.request.FILES, self.request.POST)
			currweek = getCurrentWeek()
			pg = getProjectGroupByStudentId(getStudentIdByUser(self.request.user))
			evalset = getBTPEvalSetByProjectGroup(pg)
			btpgs = getAllBTPProjectGroupsByEvalSet(evalset)
			btpsetweek = getBTPSetWeek(sets, week)
			mysubmissions = getMyGroupSubmission(pg, btpsetweek )
			context['before_deadline'] = checkBeforeDeadline(btpsetweek)
		
			context['pgid']= pg.id
			context['evalset'] = evalset
			context['btpgs'] = btpgs
			
			context['btpsetweek'] = btpsetweek
			context['usertype'] = 'students'
			context['submissions'] = mysubmissions
			
		if "FACULTY" in usertypes:
			facid = getFacultyIdByUser(self.request.user)
			week = getCurrentWeek()
			currweek = getCurrentWeek()
			pgs = getAllProjectGroupsFaculty(facid)
			evaldays = getProjectGroupEvalDay(pgs)
			sortedevaldays = sorted(evaldays, key=lambda k: k['evalday']) 
			SUBMISSIONS = []	
			for pg in pgs:
				sub = getAllSubmissionsPG(pg)
				SUBMISSIONS.append(sub)
			context['mystudentsubmissions'] = SUBMISSIONS
			context['usertype'] = 'faculty'
			context['pgs'] = pgs
			context['evaldays'] = sortedevaldays
		return context
	def dispatch(self, *args, **kwargs):
		return super(BTPIndexView,self).dispatch(*args,**kwargs)

class LoginView(FormView):
	template_name = 'accounts/login.html'
	form_class = LoginForm
	success_url = settings.LOGIN_REDIRECT_URL
	def form_valid(self,form):
		username = form.cleaned_data['username']
	    	password = form.cleaned_data['password']
    		user = authenticate(username=username, password=password)
		
    		if user is not None:
			
        		if user.is_active:
				
            			login(self.request, user)
			return HttpResponseRedirect('/')
		return super(LoginView,self).form_valid(form)
	def form_invalid(self,form):
		return render(self.request, self.template_name, {'form': form, 'form_error':'Sorry, username or password incorrect!' } )
	def get_context_data(self,**kwargs):	
		context = super(LoginView,self).get_context_data(**kwargs)
		context = {'title':'Login - Septem',
			   'form':LoginForm(self.request.POST)	
		}
		return context

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='accounts/password_change_form.html',
                    post_change_redirect = None,
                    password_change_form=ChangePasswordForm,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': ('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(settings.LOGIN_URL)

class UnderConstruction(TemplateView):
	template_name = 'index/underconstruction.html'
	def dispatch(self, *args, **kwargs):
		return super(UnderConstruction,self).dispatch(*args, **kwargs)
@csrf_exempt
def submit_report( request):
	if request.is_ajax:
		usertype = getUserTypes(request.user)
		if "STUDENT" in usertype:
	           	form = SubmissionForm(request.FILES, request.POST)
		   	print request.FILES['fileuploaded']
		   	
                	fileuploaded = request.FILES['fileuploaded']
			
			pg = getProjectGroupByStudentId(getStudentIdByUser(request.user))
			evalset = getBTPEvalSetByProjectGroup(pg)
			getAllBTPProjectGroupsByEvalSet(evalset)		
			pgid = pg.id
                        response_data = {}
			print "here"
			try:
				currweek = getCurrentWeek()
				week = BTPSetWeek.objects.get(week = currweek, sets=evalset)
				try:
					submit = BTPSubmission.objects.get(week = week , projectgroup = pg)
					submit.fileuploaded = fileuploaded
					submit.submitted_by = request.user
					send_mail(subject, message, 'btpc@iiits.in',to_list, fail_silently=False)
		
					
					submit.save()
				except ObjectDoesNotExist as error:
					
					submit = BTPSubmission( week = week , projectgroup = pg, fileuploaded = fileuploaded, submitted_by = request.user )
					subject = getSubjectMail(submit)
					message = getContentMail(submit)
					to_list = getMailingList(submit)
					
					send_mail(subject, message, 'btpc@iiits.in',to_list, fail_silently=False)
					submit.save()
					response_data['status'] = 200	
				
			except ObjectDoesNotExist as error:
				week = BTPSetWeek.objects.all()[0]
				response_data['status'] = 500
				print "Here"
		return HttpResponseRedirect('/btp')
