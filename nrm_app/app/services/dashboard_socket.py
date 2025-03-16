import time
from flask_socketio import Namespace

from app.services.utils import handle_users_data, handle_server_data


class DashboardNamespace(Namespace):
    """
    Mój socket dla dashboard (panel administracyjny)
    """
    PER_PAGE = 2
    last_data = None
    last_server_info = None
    last_samba_server_info = None
    last_resource_server_info = None

    def on_connect(self):
        print("connected")

    def on_disconnect(self):
        print("Disconnected from default namespace '/'")

    def on_what_about_server(self):
        info_response = {
            "status": "There's none data",
        }

        if self.last_data is not None:
            self.pagination_handle(users=self.last_data)
        else:
            self.emit(info_response)

        self.emit('linux_server_data_table', {"data": self.last_server_info,
                                              "status": "success"})

        self.emit('resource_linux_server_data_table', {"data": self.last_resource_server_info,
                                                 "status": "success"})

        if self.last_samba_server_info is not None:
            self.samba_server_data_pagination_handle(self.last_samba_server_info)

        else:
            self.emit('samba_server_data_table', info_response)



    def on_request_page(self, data):
        page = data.get('page')

        self.pagination_handle(
            users=self.last_data,
            page=page
        )

    def on_request_page_for_samba_server_data(self, data):
        page = data.get('page')
        self.samba_server_data_pagination_handle(
            data=self.last_samba_server_info,
            page=page
        )


    def update_dashboard_data(self, app, socketio):
        """Rozpoczęcie wątku nasłuchiwania Redis."""
        def redis_listener():
            """Sprawdź redis a nastepnie wyślij jako websocket."""
            with ((app.app_context())):
                redis_client = app.config['REDIS_CLIENT']
                while True:
                    samba_data = redis_client.get('latest_samba_metrics')
                    server_data = redis_client.get('latest_server_metrics')
                    samba_server_data = redis_client.get('latest_samba_server_metrics')
                    resource_server_data = redis_client.get('latest_most_used_processes')

                    try:
                        users = handle_users_data(samba_data)
                        server_info = handle_server_data(server_data)
                        samba_server_info = handle_server_data(samba_server_data)
                        resource_server_info = handle_server_data(resource_server_data)

                        try:
                            if users and users != self.last_data:
                                self.last_data = users
                                self.pagination_handle(users=users)
                            if samba_server_info and samba_server_info != self.last_samba_server_info:
                                try:
                                    self.last_samba_server_info = samba_server_info
                                    self.samba_server_data_pagination_handle(data=samba_server_info)
                                except Exception as e:
                                    error_response = {
                                    "status": "error",
                                    "message": f"Not working with error {str(e)}"}
                                    self.emit('samba_server_data_table', error_response)
                            if server_info and server_info != self.last_server_info:
                                self.last_server_info = server_info
                                self.emit('linux_server_data_table',
                                          {'data': server_info,
                                           'status': "success"})
                            if resource_server_info and resource_server_info != self.last_resource_server_info:
                                self.last_resource_server_info = resource_server_info
                                self.emit('resource_linux_server_data_table', {
                                    'data': resource_server_info,
                                    'status': "success"
                                })
                        except Exception as e:
                            print(f"Emitowane dane nie działają ", e)
                    except Exception as e:
                        print(f"Błąd podczas sprawdzania Redis: {e}")
                    # Poczekaj przed ponowną próbą
                    time.sleep(13)

        # start background task
        socketio.start_background_task(redis_listener)
        print("Redis listener uruchomiony w tle.")

    def pagination_handle(self, users: list, page: int=1):
        """
        funkcja do zarządzania paginacją
        """
        per_page = self.PER_PAGE
        total_pages = (len(users) + per_page - 1) // per_page
        splitted_users = [user.split() for user in users]
        start = (page - 1) * per_page
        end = start + per_page
        paginated_users = splitted_users[start:end]

        try:
            self.emit('update_users', {
                'users': paginated_users,
                'page': page,
                'total_pages': total_pages
            })
        except Exception as e:
            print("Error in update_users_emit, ", e)



    def samba_server_data_pagination_handle(self, data: dict, page: int=1):
        try:
            per_page = self.PER_PAGE

            # that's why only 3 pages. It's okay for data like that.
            total_pages = (len(data['cpu_usage']) + per_page - 1) // per_page
            start = (page - 1) * per_page
            end = start + per_page

            paginated_cpu_usage = data['cpu_usage'][start:end]
            paginated_memory_usage = data['memory_usage'][start:end]
            paginated_processes = data['processes'][start:end]

            paginated_data = {
                "cpu_usage": paginated_cpu_usage,
                "memory_usage": paginated_memory_usage,
                "processes": paginated_processes
            }

            print(f'preapre to send: {paginated_data}')

            self.emit('samba_server_data_table', {
                'data': {
                    'samba_server_data': paginated_data
                },
                'status': 'success',
                'page': page,
                'total_pages': total_pages
            })
        except Exception as e:
            print("Error in update_users_emit, ", e)
