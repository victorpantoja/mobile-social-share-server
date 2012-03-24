# coding: utf-8
#!/usr/bin/env python


def rota(route=None, controller=None, action="index", name=None, module=None):
    return [name, route, controller, action, module]

rotas = (
        rota("/applications.json", "ApplicationHandler", module="application", action="applications", name="list_apps"),
        rota("/application/subscribe", "ApplicationHandler", module="application", action="subscribe", name="subscribe"),

        rota("/context", "ContextHandler", module="context", action="index", name="context"),
        rota("/context/callback_url", "ContextTestHandler", module="context", action="callback", name="context_callback"),

        rota("/friendship/get.json", "GetFriendshipsHandler", module="friendship", action="friends", name="friends"),
        rota("/friendship/remove", "RemoveFriendshipsHandler", module="friendship", action="remove", name="remove_friend"),

        rota("/invite/send", "SendInviteHandler", module="invite", action="send", name="send_invite"),
        rota("/invite/accept", "AcceptInviteHandler", module="invite", action="accept", name="accept_invite"),
        rota("/invite/get.json", "GetInviteHandler", module="invite", action="list", name="get_invite"),
        rota("/invite/email/send", "SendEmailInviteHandler", module="invite", action="email", name="send_email"),
        rota("/invite/email/accept", "AcceptEmailInviteHandler", module="invite", action="accept_email", name="accept_email"),
        rota("/invitation/get.json", "GetInvitationHandler", module="invite", action="invitation", name="invitation"),

        rota("/user.json", "UserHandler", module="user", action="user", name="user_user"),
        rota("/user/create", "UserHandler", module="user", action="create", name="user_create"),
        rota("/user/login", "UserHandler", module="user", action="login", name="user_login"),
        rota("/user/search.json", "UserHandler", module="user", action="search", name="user_search"),

        rota("/status", "StatusHandler", module="status", action="status", name="status"),
        rota("/auth", "AuthorizationHandler", module="facebook", action="auth", name="auth"),

        #rota("/filters/maps", "MapsHandler", module="home", action="index", name="maps"),
)
