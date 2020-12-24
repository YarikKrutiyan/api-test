SECTION_ID = "select section_id from routes_routepoint " \
             "inner join field_reports_fieldreport frf on routes_routepoint.id = frf.route_point_id " \
             "inner join fields_field ff on ff.id = routes_routepoint.belong_to_field_id " \
             "where company_id = 0000 and route_id is not NULL ORDER BY ff.created_at DESC ;"

ROUT_POINT_ID = "select routes_routepoint.id from routes_routepoint " \
                "inner join field_reports_fieldreport frf on routes_routepoint.id = frf.route_point_id " \
                "inner join fields_field ff on ff.id = routes_routepoint.belong_to_field_id " \
                "where company_id = 0000 and route_id is not NULL ORDER BY ff.created_at DESC ;"

SELECT_LAND_ID = "select id from land_holders_land " \
                 "where title = 'TestQA' and deleted_at is null and company_id = 0000 " \
                 "ORDER BY created_at DESC "

SELECT_EXIST_TITLE = "select title from land_holders_land " \
         "where deleted_at is null and company_id = 0000 " \
         "ORDER BY created_at DESC "

SELECT_TARGET_FIELD_ID = "select target_field_id from analyzes_soilanalysisarea " \
         "inner join analyzes_analysis aa on aa.id = analyzes_soilanalysisarea.analysis_id " \
         "where company_id = 0000"

SELECT_COUNT_LAND = "select count(*) from land_holders_land where company_id = 0000 and deleted_at is null"

SELECT_FULL_NAME_CONTERPATY = "select fullname from contractors_counterparty where company_id = 0000"

SELECT_CONTRPARTY_ID = "select deleted_at from contractors_counterparty where id = 0000"

