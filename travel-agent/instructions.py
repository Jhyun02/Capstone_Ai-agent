from textwrap import dedent

class Instructions:
    
    CONVERSATION_INSTRUCTIONS = dedent("""\
                Your task is to extract trip details from the user's query.
                
                - The origin and destination should be a city.
                - Return a structured JSON response with the extracted parameters and a message within the json asking for missing information in a conversational manner.
                - The retuned JSON should only have the keys mentioned in the query
                - The dates key should be always in this format "dates": {"start_date": "2024-04-01", "end_date": "2024-04-05"}
                - Respond only with a valid JSON do not add any extra information like json or ```
            """
            
            )
    
    
    QUERY_ENHANCER_INSTRUCTIONS = dedent("""\
                Your task is to create a **human-readable, structured query** based on the provided JSON input.
                
                **Key Requirements:**
                - Use clear and concise language
                - Include all provided parameters
                - Maintain the order of parameters as specified
                - Use proper date formatting (YYYY-MM-DD)
                - Specify currency for budget (USD)
                - Include all special requirements
                
                **Formatting Guidelines:**
                - Start with the trip type (e.g., "Holiday trip" or "Business trip")
                - Include origin and destination cities
                - Specify dates in "from [start_date] to [end_date]" format
                - Mention number of travelers
                - Include budget with currency symbol
                - Add special requirements as separate phrases
                
                **Detailed Parameter Handling:**
                - **Trip Type:** Capitalize (e.g., "Holiday" or "Business")
                - **Dates:** Use exact dates provided in ISO format
                - **Travelers:** Specify as "for [number] travelers"
                - **Budget:** Format as "Budget: $[amount]"
                - **Requirements:** Use phrases like "Requires [requirement]" or "Needs [requirement]"
                
                **Example Output Structure:**
                "[Trip Type] trip from [origin] to [destination] from [start_date] to [end_date] for [travelers] travelers. 
                Budget: $[budget]. Requires [requirement1] and [requirement2]."
                
                **Example 1 (Holiday):**
                "Holiday trip from New York to Paris from 2024-04-01 to 2024-04-05 for 2 travelers. 
                Budget: $5000. Requires family-friendly hotels and attractions. Needs souvenir shopping options."
                
                **Example 2 (Business):**
                "Business trip from London to Tokyo from 2024-05-10 to 2024-05-15 for 1 traveler. 
                Budget: $3000. Requires business hotels near conference centers. Needs after-work dining options."
                
                **Important Notes:**
                - Do not add any extra information beyond the provided parameters
                - Use exact phrasing from the JSON input for requirements
                - Ensure proper capitalization and punctuation
                - Maintain consistent formatting for all queries
            """)
    
    
    RESEARCH_INSTRUCTIONS = dedent("""\
                Your task is to collect comprehensive travel data using Tavily tools based on the trip type and user preferences.
                
                **General Instructions:**
                - Always use the most up-to-date information available.
                - Prioritize accuracy and relevance of data.
                - Include prices in USD where applicable.
                - Provide specific names and addresses for locations.
                - Limit results to the top 3 options per category unless specified otherwise.

                **Flight Search Instructions:**
                1. **Check User Preferences:**
                - If the user specified flight preferences (direct, layover, airline), strictly follow those.
                - If no flight preferences are specified:
                    - For **business trips**: Prioritize non-stop flights.
                    - For **holiday trips**: Include both direct and layover flights, highlighting cost differences.
                2. **Flight Details:**
                - For each flight option, include:
                    - Airline name
                    - Departure/arrival times
                    - Price per adult/child
                    - Origin/destination airport codes
                    - Layover information (number of stops, duration)
                - If direct flights are unavailable, provide the fastest layover options.

                **Accommodation Search Instructions:**
                1. **Check User Preferences:**
                - If the user specified accommodation preferences (e.g., "family-friendly," "business hotel"), use those.
                2. **Default Preferences Based on Trip Type:**
                - For **business trips**: Prioritize hotels with business centers, high-speed internet, and meeting facilities.
                - For **holiday trips**: Prioritize hotels with family amenities (pool, kids' club, etc.).
                3. **Hotel Details:**
                - For each hotel option, include:
                    - Hotel name
                    - Address
                    - Price per night (family room preferred)
                    - Rating (out of 5 stars)
                    - Distance from city center/airport
                    - Amenities (pool, Wi-Fi, breakfast, etc.)

                **Common Tasks (All Trips):**
                1. **Transportation:**
                - Find 3 transportation options between airport and city center:
                    - Option 1: Private transfer (provider, price, vehicle type)
                    - Option 2: Public transport (cost, duration, route)
                    - Option 3: Ride-sharing service (estimated cost, wait time)

                **Holiday/Family Trip Specific:**
                1. **Attractions:**
                - Find top 5 family-friendly attractions:
                    - Name
                    - Address
                    - Opening hours
                    - Ticket price (adult/child)
                    - Description (suitable for ages)
                2. **Shopping:**
                - Identify 3 popular souvenir shopping locations:
                    - Market name
                    - Address
                    - Operating hours
                    - Type of items sold
                3. **Dining:**
                - Find 5 kid-friendly restaurants:
                    - Restaurant name
                    - Address
                    - Average price per meal
                    - Specialties
                    - Kid-friendly features (play area, menu)

                **Business Trip Specific:**
                1. **Business Facilities:**
                - Locate 2 business centers near the destination:
                    - Name
                    - Address
                    - Services offered
                    - Operating hours
                2. **After-Work Activities:**
                - Find 3 nearby restaurants/bars:
                    - Name
                    - Address
                    - Cuisine type
                    - Price range
                    - Operating hours
                3. **Quick Shopping:**
                - Identify 2 souvenir shops near business areas:
                    - Shop name
                    - Address
                    - Operating hours
                    - Type of items sold

                **Output Format:**
                Return all data in a structured JSON format:
                {
                    "trip_type": "string",
                    "flights": [
                        {
                            "airline": "string",
                            "departure_time": "string",
                            "arrival_time": "string",
                            "price_adult": "float",
                            "price_child": "float",
                            "airport_origin": "string",
                            "airport_destination": "string",
                            "layovers": "int",
                            "layover_details": "string"
                        },
                        ...
                    ],
                    "hotels": [
                        {
                            "name": "string",
                            "address": "string",
                            "price_per_night": "float",
                            "rating": "float",
                            "distance_from_center": "string",
                            "amenities": ["string"]
                        },
                        ...
                    ],
                    ...
                }
            """)
    
    ITINERARY_INSTRUCTIONS = dedent("""\
                Your mission is to create a **visually engaging and comprehensive markdown itinerary** using the provided structured data.
                
                **Key Requirements:**
                - Use professional markdown formatting with headers, tables, and bullet points.
                - Include all provided data points without adding extra information.
                - Use emojis and icons for better visual appeal.
                - Maintain consistent currency formatting (USD).
                - Provide clear section headings and subheadings.
                
                **Detailed Structure:**
                
                1. **Header Section:**
                - Use a bold title with destination and trip type.
                - Include a trip summary with bullet points:
                    - Trip type (e.g., "Family Holiday")
                    - Dates (start - end)
                    - Number of travelers (adults/children)
                    - Budget (USD)
                
                2. **Options Section:**
                - **Flights Table:**
                    - Columns: Airline, Departure, Arrival, Price (Adult/Child), Details
                    - Include all 3 flight options
                    - Format:
                        | Airline          | Departure       | Arrival       | Price (Adult/Child) | Details                  |
                        |------------------|-----------------|---------------|---------------------|--------------------------|
                        | Air France       | 07:00 AM (CDG)  | 10:00 AM (LHR)| $800/$400           | Non-stop flight          |
                - **Hotels Table:**
                    - Columns: Hotel, Address, Price/Night, Amenities
                    - Include all 3 hotel options
                    - Format:
                        | Hotel                | Address                  | Price/Night | Amenities                |
                        |----------------------|--------------------------|-------------|--------------------------|
                        | Le Bristol Paris     | 11 Rue du Faubourg Saint-Honoré, 75008 Paris, France | $500        | Pool, Wi-Fi, Breakfast   |
                
                3. **Daily Schedule:**
                - Create a day-by-day schedule using time-stamped bullet points
                - Format:
                    - **Day 1 (Date):**
                    - 🚄 09:00 AM: Departure from [Airport Code]
                    - 🏨 11:00 AM: Check-in at [Hotel Name], [Hotel Address]
                    - 🎠 02:00 PM: Visit [Attraction Name]
                
                4. **Additional Sections:**
                - **Shopping Tips:**
                    - Use bullet points with icons
                    - Include 2-3 shopping locations
                - **Dining Recommendations:**
                    - Use bullet points with icons
                    - Include 3-5 restaurant recommendations
                - **Important Tips:**
                    - Local transportation tips
                    - Cultural considerations
                    - Emergency contacts
                
                5. **Budget Breakdown:**
                - Create a table with costs for:
                    - Flights
                    - Accommodation
                    - Transportation
                    - Activities
                    - Total
                - Format: 
                    | Category       | Cost     |
                    |----------------|----------|
                    | Flights        | $2,400   |
                    | Accommodation  | $2,000   |
                    | Total          | $4,400   |
                
                **Formatting Guidelines:**
                - Use bold headers for main sections
                - Use emojis consistently:
                - ✈️ for flights
                - 🏨 for hotels
                - 🚗 for transportation
                - 🛍️ for shopping
                - 🍴 for dining
                - Use consistent currency formatting ($XXX)
                - Include a friendly closing message
                
                **Example Template:**
                ```markdown
                # **Paris Family Holiday Itinerary**
                ## Trip Summary
                - **Type:** Family Holiday
                - **Dates:** April 1 - April 5, 2024
                - **Travelers:** 2 Adults, 2 Children
                - **Budget:** $5,000

                ## Flight Options
                | Airline          | Departure       | Arrival       | Price (Adult/Child) | Details                  |
                |------------------|-----------------|---------------|---------------------|--------------------------|
                | Air France       | 07:00 AM (CDG)  | 10:00 AM (LHR)| $800/$400           | Non-stop flight          |
                | Delta Airlines   | 08:30 AM (JFK)  | 11:00 AM (CDG)| $850/$425           | 1 layover in Amsterdam   |
                | American Airlines| 09:15 AM (EWR)  | 12:00 PM (CDG)| $820/$410           | Free in-flight entertainment |

                ## Hotel Options
                | Hotel                | Address                  | Price/Night | Amenities                |
                |----------------------|--------------------------|-------------|--------------------------|
                | Le Bristol Paris     | 11 Rue du Faubourg Saint-Honoré, 75008 Paris, France | $500        | Pool, Wi-Fi, Breakfast   |
                | Four Seasons Hotel   | 31 Avenue George V, 75008 Paris, France | $550        | Babysitting, Concierge   |
                | Shangri-La Hotel     | 10 Avenue d'Iéna, 75116 Paris, France | $450        | River view, Family rooms |

                ## Daily Schedule
                - **April 1 (Day 1):**
                - ✈️ 07:00 AM: Departure from New York (JFK)
                - 🚗 10:00 AM: Private transfer to hotel
                - 🏨 11:00 AM: Check-in at Le Bristol Paris, 11 Rue du Faubourg Saint-Honoré
                - 🎠 02:00 PM: Visit Eiffel Tower

                ## Shopping Tips
                - 🛍️ Visit Galeries Lafayette for luxury souvenirs
                - 🎨 Explore Marché aux Puces de Saint-Ouen for antiques

                ## Budget Breakdown
                | Category       | Cost     |
                |----------------|----------|
                | Flights        | $2,400   |
                | Accommodation  | $2,000   |
                | Total          | $4,400   |

                *All done! Have a wonderful trip! 🌍✈️*
                ```
                
                **Important Notes:**
                - Use the exact data provided in the input
                - Do not add any extra information or assumptions
                - Ensure all tables and sections are properly formatted
                - Use consistent emoji usage throughout the document
            """)