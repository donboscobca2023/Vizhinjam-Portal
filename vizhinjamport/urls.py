from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing, name='landing'),
    path('regs', views.reg, name='reg'),
    path('register_user',views.register_user,name='register_user'),
    path('register_company',views.register_company,name='register_company'),
    path('register_contractor',views.register_contractor,name='register_contractor'),
    path('user_list',views.user_list,name='user_list'),
    path('company_list',views.company_list,name='company_list'),
    path('contractor_list',views.contractor_list,name='contractor_list'),
    path('userlogin',views.login,name='userlogin'),
    path('userhome',views.userhome,name='userhome'),
    path('companyhome',views.companyhome,name='companyhome'),
    path('contractorhome',views.contractorhome,name='contractorhome'),
    path('register_ship',views.register_ship,name='register_ship'),
    path('ship_list',views.ship_list,name='ship_list'),
    path('edit_ship/<int:id>/',views.edit_ship,name='edit_ship'),
    path('delete_ship/<int:id>/',views.delete_ship,name='delete_ship'),
    path('ship_user',views.search_ship,name='ship_user'),
    path('edit_user',views.edit_user,name='edit_user'),
    path('edit_company',views.edit_company,name='edit_company'),
    path('edit_contractor',views.edit_contractor,name='edit_contractor'),
    path('export/<int:id>/',views.export,name='export'),
    path('export_list',views.export_list,name='export_list'),
    path('edit_export/<int:id>/',views.edit_export,name='edit_export'),
    path('cancel_export/<int:id>/',views.cancel_export,name='cancel_export'),
    path('export_comp_list',views.export_comp_list,name='export_comp_list'),
    
    path('refund_export/<int:id>/',views.refund_export,name='refund_export'),
    path('addnews',views.addnews,name='addnews'),
    path('admin_news_list',views.admin_news_list,name='admin_news_list'),
    path('edit_news/<int:id>/',views.edit_news,name='edit_news'),
    path('delete_news/<int:id>/',views.delete_news,name='delete_news'),
    path('news_list',views.news_list,name='news_list'),
    path('user_news_list',views.user_news_list,name='user_news_list'),
    path('company_news_list',views.company_news_list,name='company_news_list'),
    path('contractor_news_list',views.contractor_news_list,name='contractor_news_list'),

    path('Ship_track/<int:id>/',views.ship_track,name='ship_track'),
    path('Ship_track_list/<int:id>/',views.ship_track_list,name='ship_track_list'),
    path('edit_ship_track/<int:id>/<int:sid>/',views.edit_ship_track,name='edit_ship_track'),
    path('delete_ship_track/<int:id>/<int:sid>/',views.delete_ship_track,name='delete_ship_track'),
    path('user_track_ship/<int:id>/',views.user_track_ship,name='user_track_ship'),


    path('admin_header',views.admin_header,name='admin_header'),
    path('company_approve/<int:id>/',views.company_approve,name='company_approve'),
    path('company_reject/<int:id>/',views.company_reject,name='company_reject'),
    path('contractor_approve/<int:id>/',views.contractor_approve,name='contractor_approve'),
    path('contractor_reject/<int:id>/',views.contractor_reject,name='contractor_reject'),
    
    path('exportcharges',views.exportcharges,name='exportcharges'),
    path('exportcharges_list',views.exportcharges_list,name='exportcharges_list'),
    path('edit_exportcharges/<int:id>/',views.edit_exportcharges,name='edit_exportcharges'),
    path('delete_exportcharges/<int:id>/',views.delete_exportcharges,name='delete_exportcharges'),

    path('payment/<int:pid>/',views.payment,name='payment'),
    path('complaint/<int:eid>/',views.register_complaint,name='complaint'),
    path('complaint_list',views.complaint_list,name='complaint_list'),
    path('edit_complaint/<int:id>/',views.edit_complaint,name='edit_complaint'),
    path('complaint_complist/<int:id>/',views.complaint_complist,name='complaint_complist'),
    path('reply/<int:id>/',views.reply,name='reply'),
    
    path('register_tender',views.register_tender,name='register_tender'),
    path('tender_list',views.tender_list,name='tender_list'),
    path('edit_tender/<int:id>/',views.edit_tender,name='edit_tender'),
    path('delete_tender/<int:id>/',views.delete_tender,name='delete_tender'),
    path('contractor_tender_list',views.contractor_tender_list,name='contractor_tender_list'),
    path('apply_tender/<int:tid>/',views.apply_tender,name='apply_tender'),
    path('admin_applied_tender_list/<int:id>/',views.admin_applied_tender_list,name='admin_applied_tender_list'),
    
    path('apply_tender_list',views.apply_tender_list,name='apply_tender_list'),
    path('edit_apply_tender/<int:id>/',views.edit_apply_tender,name='edit_apply_tender'),
    path('delete_apply_tender/<int:id>/',views.delete_apply_tender,name='delete_apply_tender'),
    path('tender_approve/<int:id>/',views.tender_approve,name='tender_approve'),
    path('tender_reject/<int:id>/',views.tender_reject,name='tender_reject'),
    
    path('register_temp_job',views.register_temp_job,name='register_temp_job'),
    path('temp_job_list',views.temp_job_list,name='temp_job_list'),
    path('edit_temp_job/<int:id>/',views.edit_temp_job,name='edit_temp_job'),
    path('delete_temp_job/<int:id>/',views.delete_temp_job,name='delete_temp_job'),
    
    path('user_temp_job_list',views.user_temp_job_list,name='user_temp_job_list'),
    path('temp_job_apply/<int:jid>/',views.temp_job_apply,name='temp_job_apply'),
    path('user_applied_job_list',views.user_applied_job_list,name='user_applied_job_list'),
    path('edit_user_applied_job/<int:id>/',views.edit_user_applied_job,name='edit_user_applied_job'),
    path('delete_user_applied_job/<int:id>/',views.delete_user_applied_job,name='delete_user_applied_job'),
    
    path('admin_applied_job_list/<int:id>/',views.admin_applied_job_list,name='admin_applied_job_list'),
    path('temp_job_approve/<int:id>/<int:jid>/',views.temp_job_approve,name='temp_job_approve'),
    path('temp_job_reject/<int:id>/<int:jid>/',views.temp_job_reject,name='temp_job_reject'),
    
    path('register_interview/<int:id>/',views.register_interview,name='register_interview'),
    path('interview_list/<int:id>/',views.interview_list,name='interview_list'),
    path('edit_interview/<int:id>/<int:lid>',views.edit_interview,name='edit_interview'),
    path('delete_interview/<int:id>/<int:lid>',views.delete_interview,name='delete_interview'),
    path('interview_user/<int:id>/',views.interview_user,name='interview_user'),
    
    path('logout',views.logout,name='logout'),
    
    path('company_complaint',views.company_complaint,name='company_complaint'),
    path('company_complaint_list',views.company_complaint_list,name='company_complaint_list'),
    path('edit_company_complaint/<int:id>/',views.edit_company_complaint,name='edit_company_complaint'),
    path('delete_company_complaint/<int:id>/',views.delete_company_complaint,name='delete_company_complaint'),

    path('user_complaint',views.user_complaint,name='user_complaint'),
    path('user_complaint_list',views.user_complaint_list,name='user_complaint_list'),
    path('edit_user_complaint/<int:id>/',views.edit_user_complaint,name='edit_user_complaint'),
    path('delete_user_complaint/<int:id>/',views.delete_user_complaint,name='delete_user_complaint'),

    path('contractor_complaint',views.contractor_complaint,name='contractor_complaint'),
    path('contractor_complaint_list',views.contractor_complaint_list,name='contractor_complaint_list'),
    path('edit_contractor_complaint/<int:id>/',views.edit_contractor_complaint,name='edit_contractor_complaint'),
    path('delete_contractor_complaint/<int:id>/',views.delete_contractor_complaint,name='delete_contractor_complaint'),

    path('admin_all_complaint_list',views.admin_all_complaint_list,name='admin_all_complaint_list'),
    path('admin_reply/<int:id>/',views.admin_reply,name='admin_reply'),
    # added by me
    path('subheader',views.subhead,name='subheader'),
    path('loginnew',views.loginnew,name='login'),
    # path('delete/<int:id>/',views.delete,name='delete'),
    path('dash',views.admin_dash,name='dash'),
    path('admin_head',views.admin_head,name='admin_head'),
    path('user_subheader',views.user_subhead,name='user_subheader'),
    path('company_subheader',views.company_subhead,name='company_subheader'),
    path('contractor_subheader',views.contractor_subhead,name='contractor_subheader'),
    # path('interview_details',views.interview_details, name='interview_details'),

    path('interview_conducting/<int:id>',views.interview_conducting, name='interview_conducting'),
    path('save_video_url/', views.save_video_url, name='save_video_url'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)