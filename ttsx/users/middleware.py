class UrlMiddleware:

    def process_view(self,request,view_name,view_args,view_kwargs):
        print '-----------%s' % request.get_full_path()
        if request.path not in['/user/register/',
                               '/user/register_handle',
                               '/user/register_yz/',
                               '/user/login/',
                               '/user/login_handle/',
                               '/user/loginout/',
                               ]:
            request.session['url_path'] = request.get_full_path()