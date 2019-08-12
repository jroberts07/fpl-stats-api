# FPL STATS API

The purpose of this project is to provide an API that connects to the FPL API and produces useful data that can be used to create graphs, tables or whatever ideas people have. This is just an API and it's purpose is to return JSON in a useful form. I am hoping people will then use this API to do more interesting things with the data. Please read the spec to see how to query the API and what data will be returned.

# Design Methodology

This may change as the API evolves but the current design methodology is this:

 - The API should be built following the micro service design principles and crucially that each request should be independent of all others.
 - The API uses the async python framework Sanic. For more complex statistics multiple FPL API endpoints will need to be called and the data processing may involve complex loops. Thus async is required to keep processing time to a minimum.
 - A mongoDB has been attached in the Dockerfile. This is currently unused but the rationale behind it is that some static data from the FPL API may be able to be stored here and only needs updating when there is a data reload (often weekly). This would save making requests to the FPL API on every request.

# Usage

To run the API you will need Docker installed. Then clone the repo and type:

    make run
 
 You can then make requests to the api by using the following endpoint:
 

    http://127.0.0.1:30000/entry_data/{entry_id}?player_id={player_id}

Please read the spec for more endpoints.

The entry_id can be obtained by visiting the [FPL website](https://fantasy.premierleague.com/) and going to your points page. The entry_id is then present in the URL. The player_id can be obtained by opening the cookies and copying the on named pl_profile.

# Contribution

Please feel free to raise issues if you have new endpoints you'd like to see or think there are ways the current code can be improved. Or even better submit PRs yourself. Each new endpoint should be accompanied with python doc comments, unit & functional tests and and an update to the spec.
