## Traceability System

*En Desarrollo*

* Server: NodeJs, Express, PostgreSQL
	* Env Vars:
		* PGUSER
		* PGHOST
		* PGPASSWORD
		* PGDATABASE
		* PGPORT

* Web: Django, PostgreSQL
	* Env Vars:
		* WEB_PGUSER
		* WEB_PGHOST
		* WEB_PGPASSWORD
		* WEB_PGDATABASE
		* WEB_PGPORT
		* TRACE_PGUSER
		* TRACE_PGHOST
		* TRACE_PGPASSWORD
		* TRACE_PGDATABASE
		* TRACE_PGPORT
		* DJANGO_SECRET_KEY

* Client: Custom Python library
	* Env Vars:
		* TRACEABILITY_API_URL
