from .location_within_radius import get_all_within_radius as all_cities


@jobs_bp.route('', methods=['GET'])
def get_jobs():
    title_query = request.args.get('title')
    location_query = request.args.get('location')
    company_query = request.args.get('company')
    days_ago = request.args.get('days_ago', type=int)
    
    
    query = db.session.query(Job).join(Data).options(joinedload(Job.data)).order_by(Data.fetch_date.desc())


    radius = request.args.get('r', type=int)
    if not location_query or 'remote' in location_query:
        if title_query:
            new_query = new_query.filter(Job.title.ilike('%'+title_query.strip()+'%'))
        if company_query:
            new_query = new_query.filter(Job.company.ilike('%'+company_query.strip()+'%'))
        if days_ago:
            posted_date = func.current_date() - timedelta(days=int(days_ago))
        
        # Convert to the same format as the fetch_date in the database
        posted_date_str = posted_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        new_query = new_query.filter(Data.fetch_date >= posted_date_str)

        # Execute the final query
        jobs.append(query.all())
    else:
        if radius:
            location_area = (location_query , radius)
        else:
            location_area = (location_query)
            
        jobs = []
        for city in location_area:
            new_query = query
            if title_query:
                new_query = new_query.filter(Job.title.ilike('%'+title_query.strip()+'%'))
            if location_query:
                new_query = new_query.filter(Job.location.ilike('%'+city.strip()+'%'))
            if company_query:
                new_query = new_query.filter(Job.company.ilike('%'+company_query.strip()+'%'))
            if days_ago:
                posted_date = datetime.utcnow() - timedelta(days=int(days_ago))
            
            # Convert to the same format as the fetch_date in the database
            posted_date_str = posted_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            new_query = new_query.filter(Data.fetch_date >= posted_date_str)

            # Execute the final query
            jobs.append(query.all())