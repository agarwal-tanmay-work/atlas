def get_seed_failures() -> list[dict]:
    failures = [
        # Software Engineering (1-10)
        {
            "title": "Knight Capital Group Trading Glitch",
            "domain": "Software Engineering",
            "subdomain": "Algorithmic Trading",
            "year": 2012,
            "organization": "Knight Capital Group",
            "what_failed": "A repurposed flag in an automated trading system activated obsolete, dead code during deployment, executing 4 million invalid trades in 45 minutes.",
            "root_cause": "Dead code was left in the system for years and an old feature flag was repurposed. The deployment was manual and missed 1 of 8 servers.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Manual deployment of critical system without automated checks",
                "Leaving unused, untested 'dead code' in the production codebase",
                "Lack of automated volume limits or 'kill switches' for rogue trading algorithms",
                "Alerts during first minutes were ignored as 'normal noise'"
            ],
            "what_was_done_wrong": "Engineers reused an old flag instead of creating a new one, triggering an old algorithm that bought high and sold low. The deployment process lacked verification.",
            "how_it_was_fixed": "The system was taken offline, but the company lost $440 million and was essentially bankrupt within an hour.",
            "lesson": "Never leave dead code in production, never reuse feature flags, and automate your deployments.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Knight_Capital_Group",
            "tags": ["Deployment", "Dead Code", "Feature Flags", "Trading"]
        },
        {
            "title": "Amazon S3 US-East-1 Outage",
            "domain": "Software Engineering",
            "subdomain": "Cloud Infrastructure",
            "year": 2017,
            "organization": "Amazon Web Services",
            "what_failed": "An engineer investigating an issue incorrectly entered a command typo, taking down a massive portion of the S3 billing and indexing systems, which brought down half the internet.",
            "root_cause": "The command line interface allowed a typo to execute a destructively wide command without confirmation or rate limiting.",
            "root_cause_category": "Human Error",
            "warning_signs": [
                "Tooling allowed raw shell commands against critical routing infrastructure",
                "No safety guardrails confirming bulk removal commands",
                "S3 subsystems dependencies were deeply coupled to S3 functioning itself"
            ],
            "what_was_done_wrong": "A typo in a playbook command. More importantly, the system lacked blast radius limits and allowed a human single point of failure.",
            "how_it_was_fixed": "AWS rebooted the index subsystems. They later updated their tooling to require safety confirmations and rate limits for capacity removal.",
            "lesson": "Design human-friendly tooling with safety rails. Humans will make typos; the system should not collapse because of one.",
            "severity": "Critical",
            "source_url": "https://aws.amazon.com/message/41926/",
            "tags": ["Typo", "Cloud", "Tooling", "Blast Radius"]
        },
        {
            "title": "GitLab Production Database Deletion",
            "domain": "Software Engineering",
            "subdomain": "Databases",
            "year": 2017,
            "organization": "GitLab",
            "what_failed": "An engineer accidentally ran `rm -rf` on the production database directory instead of the staging database directory.",
            "root_cause": "Production and staging environments were accessed using similar windows/terminal setups, leading to context confusion. Furthermore, 5 out of 5 backup mechanisms failed or were untested.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Backups were reporting success but were actually returning empty files",
                "No distinct styling or warnings between production and staging terminals",
                "Engineer was fighting late-night fatigue while running operations"
            ],
            "what_was_done_wrong": "Executed a destructive command in the wrong window. Failed to ever test the automated backup restoration process.",
            "how_it_was_fixed": "The site was restored 18 hours later from a 6-hour-old manual local backup an engineer happened to take.",
            "lesson": "A backup isn't a backup until you've successfully restored from it. Environments need hard visual distinction.",
            "severity": "High",
            "source_url": "https://about.gitlab.com/blog/2017/02/01/gitlab-dot-com-database-incident/",
            "tags": ["Database", "Backups", "Terminal", "Human Error"]
        },
        {
            "title": "Cloudflare Global Outage",
            "domain": "Software Engineering",
            "subdomain": "Networking",
            "year": 2019,
            "organization": "Cloudflare",
            "what_failed": "A poorly written Regex deployed to the WAF caused a catastrophic CPU spike across all edge nodes worldwide, dropping 82% of global traffic.",
            "root_cause": "The regex rule `(?:(?:\"|'|]|}|\\\\|d|(?:nan|infinity|true|false|null|undefined|symbol|math)|\\`|\\-)\\s*\\+` caused catastrophic backtracking on payload evaluation.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "Testing pipeline did not verify regex CPU consumption on diverse payloads",
                "Global deployment hit all servers simultaneously instead of a phased rollout",
                "No automatic circuit breaker for WAF rule processing limits"
            ],
            "what_was_done_wrong": "Pushed an unoptimized regex without staged rollout or performance guarantees.",
            "how_it_was_fixed": "The WAF rule was globally reverted manually by engineers. Rollout processes were changed to phased execution.",
            "lesson": "Deployments must be phased, and regular expressions are dangerous code that require strict performance bounds.",
            "severity": "Critical",
            "source_url": "https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/",
            "tags": ["Networking", "Regex", "CPU Spike", "WAF"]
        },
        {
            "title": "Facebook 6-Hour Global Outage",
            "domain": "Software Engineering",
            "subdomain": "Networking",
            "year": 2021,
            "organization": "Facebook / Meta",
            "what_failed": "A BGP routing command mistakenly disconnected Facebook's entire network footprint from the internet, taking down Facebook, Instagram, and WhatsApp.",
            "root_cause": "An automated configuration audit tool contained a bug. When engineers issued a command to assess backbone capacity, it unintentionally severed all BGP routes globally.",
            "root_cause_category": "Single Point of Failure",
            "warning_signs": [
                "Building internal tools that have the capability to sever all routes simultaneously",
                "Internal DNS and physical door badge systems were on the identical network segment, locking engineers out of the building during the crisis"
            ],
            "what_was_done_wrong": "The internal tool lacked sanity checks for pulling 100% of routes. Physical and logical access relied on the same single dependency.",
            "how_it_was_fixed": "Engineers had to physically break into data centers with angle grinders to access console ports and manually reconfigure routers.",
            "lesson": "Never place critical out-of-band management and physical access on the very network they are meant to manage.",
            "severity": "Critical",
            "source_url": "https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/",
            "tags": ["BGP", "DNS", "Networking", "Out-of-band"]
        },
        {
            "title": "Twitter's Fail Whale Era",
            "domain": "Software Engineering",
            "subdomain": "Architecture",
            "year": 2008,
            "organization": "Twitter",
            "what_failed": "Twitter experienced daily outages represented by the 'Fail Whale' image due to sheer user volume overwhelming their Ruby on Rails monolithic architecture.",
            "root_cause": "The initial architecture was a single monolithic web application supported by a single master database, which could not scale to the fan-out read-write patterns of social media.",
            "root_cause_category": "Scaling Failure",
            "warning_signs": [
                "Spikes in concurrent read/write queries during global events causing total DB lockup",
                "Band-aid solutions like increased hardware repeatedly failed",
                "High latency on the core message bus"
            ],
            "what_was_done_wrong": "Continued patching the monolith rather than pausing to fundamentally re-architect the data fan-out model sooner.",
            "how_it_was_fixed": "Migrated to a JVM-based microservices architecture (Scala/Finagle) and implemented separate fan-out message queues for feed generation.",
            "lesson": "Architecture that works for 10,000 users will fundamentally break at 10,000,000. Rewrite is sometimes the only path.",
            "severity": "High",
            "source_url": "https://blog.twitter.com/engineering/en_us/a/2013/new-tweets-per-second-record-and-how",
            "tags": ["Monolith", "Scaling", "Database", "Microservices"]
        },
        
        # Aviation (11-16)
        {
            "title": "Air France Flight 447",
            "domain": "Aviation",
            "subdomain": "Commercial",
            "year": 2009,
            "organization": "Air France",
            "what_failed": "The aircraft stalled and crashed into the Atlantic Ocean after pitot tubes froze, disconnecting the autopilot and confusing the pilots.",
            "root_cause": "Pilots lacked training in manual high-altitude stalls. They pulled back on the stick instead of pushing forward, maintaining the aerodynamic stall into the ocean.",
            "root_cause_category": "Human Error",
            "warning_signs": [
                "Repeated stall warnings sounding in the cockpit",
                "Contradictory airspeed readings",
                "Co-pilot continuously pulling nose up despite stall warnings"
            ],
            "what_was_done_wrong": "Over-reliance on automated systems led to degradation of basic aviator skills (pitch and power). The crew failed to communicate who was in control.",
            "how_it_was_fixed": "Mandated improved high-altitude stall recovery training and redesigned pitot tubes.",
            "lesson": "When automation fails, you must know how to fly the plane manually. Fundamentals matter more than systems.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Air_France_Flight_447",
            "tags": ["Automation", "Training", "Sensors"]
        },
        {
            "title": "Tenerife Airport Disaster",
            "domain": "Aviation",
            "subdomain": "Commercial",
            "year": 1977,
            "organization": "KLM / Pan Am",
            "what_failed": "Two Boeing 747s collided on a foggy runway, killing 583 people in the deadliest aviation accident in history.",
            "root_cause": "The KLM captain initiated takeoff without explicit clearance from ATC due to radio interference, urgency, and non-standard phraseology.",
            "root_cause_category": "Communication Breakdown",
            "warning_signs": [
                "Heavy fog reducing visibility to near zero",
                "Heterodyne radio interference stepping on critical transmissions",
                "Flight engineer expressed doubt that the runway was clear, but was overruled by the senior captain"
            ],
            "what_was_done_wrong": "Captain assumed clearance rather than verifying. Rigid authority structure prevented subordinates from intervening effectively.",
            "how_it_was_fixed": "Implementation of standard aviation phraseology (e.g., 'Takeoff' only used for actual clearance) and Crew Resource Management (CRM).",
            "lesson": "Ambiguity in communication is deadly. Empower subordinates to speak up against authority.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Tenerife_airport_disaster",
            "tags": ["Communication", "Authority Bias", "Fog", "CRM"]
        },
        {
            "title": "Alaska Airlines Flight 261",
            "domain": "Aviation",
            "subdomain": "Maintenance",
            "year": 2000,
            "organization": "Alaska Airlines",
            "what_failed": "The horizontal stabilizer jackscrew failed in flight, causing an uncontrollable dive into the Pacific Ocean.",
            "root_cause": "Extreme wear and lack of lubrication on the tail jackscrew threads due to deferred maintenance and extended inspection intervals to cut costs.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Mechanic previously noted the part needed replacement but was overridden by management",
                "Lubrication intervals were extended far beyond manufacturer recommendations",
                "Aircraft exhibited pitch control issues on previous flights"
            ],
            "what_was_done_wrong": "Prioritized extending maintenance schedules to save money over safety. Ignored whistleblowers.",
            "how_it_was_fixed": "The FAA mandated stricter inspection protocols and lubrication intervals for jackscrews.",
            "lesson": "Cost-cutting on maintenance inevitably leads to systemic collapse. Listen to front-line workers.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Alaska_Airlines_Flight_261",
            "tags": ["Maintenance", "Cost-Cutting", "Whistleblower"]
        },
        {
            "title": "United Airlines Flight 173",
            "domain": "Aviation",
            "subdomain": "Commercial",
            "year": 1978,
            "organization": "United Airlines",
            "what_failed": "A DC-8 ran out of fuel and crashed in a suburban neighborhood while the crew troubleshot a minor landing gear indicator light.",
            "root_cause": "The captain became utterly fixated on a burnt-out landing gear light, ignoring the flight engineer's repeated calculations that they were out of fuel.",
            "root_cause_category": "Ignored Warning Signs",
            "warning_signs": [
                "Flight engineer explicitly stating fuel levels were critically low",
                "Engines flaming out one by one",
                "Holding pattern lasted 1 hour for a minor mechanical check"
            ],
            "what_was_done_wrong": "Target fixation. The crew forgot the primary directive: fly the airplane.",
            "how_it_was_fixed": "This crash directly led to the universal adoption of Crew Resource Management (CRM) in aviation worldwide.",
            "lesson": "Don't focus so intensely on a minor bug that you ignore the system crashing around you.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/United_Airlines_Flight_173",
            "tags": ["Fixation", "Fuel", "CRM"]
        },
        {
            "title": "Boeing 737 MAX MCAS",
            "domain": "Aviation",
            "subdomain": "Engineering",
            "year": 2019,
            "organization": "Boeing",
            "what_failed": "Two brand new 737 MAX aircraft crashed within 5 months due to an automated flight control system (MCAS) forcing the nose down repeatedly.",
            "root_cause": "MCAS relied on a single Angle of Attack (AoA) sensor without redundancy. Training manuals hid the existence of MCAS to avoid regulatory simulator requirements.",
            "root_cause_category": "Single Point of Failure",
            "warning_signs": [
                "Engineers raised concerns about a single point of failure but were silenced",
                "Lion Air crew reported runaway trim the day before the first fatal crash",
                "Pressure from Airbus A320neo timeline drove rushed development"
            ],
            "what_was_done_wrong": "Management prioritized avoiding expensive simulator training over safety, hiding critical system architecture from pilots.",
            "how_it_was_fixed": "Fleet grounded for 20 months. MCAS was rewritten to read from dual sensors and pilot training was heavily mandated.",
            "lesson": "Never hide system behavior from the end-user, and never wire safety-critical systems to a single sensor.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Boeing_737_MAX_grounding",
            "tags": ["Sensors", "Automation", "Cover-Up", "Economics"]
        },
        {
            "title": "Japan Airlines Flight 123",
            "domain": "Aviation",
            "subdomain": "Maintenance",
            "year": 1985,
            "organization": "Japan Airlines",
            "what_failed": "Explosive decompression blew off the vertical stabilizer, rendering the Boeing 747 uncontrollable and resulting in 520 deaths.",
            "root_cause": "An improper repair on the rear pressure bulkhead 7 years prior. The technicians used a single row of rivets instead of two, halving the metal's fatigue resistance.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Boeing repair guidelines explicitly required a double row of rivets",
                "Micro-cracks were forming in the bulkhead for years during pressurization cycles"
            ],
            "what_was_done_wrong": "Technicians took a shortcut on a critical structural repair. Inspectors failed to catch the deviation from the manual.",
            "how_it_was_fixed": "Massive overhaul of maintenance inspection procedures across all Boeing aircraft.",
            "lesson": "A small deviation from protocol in a complex system can lay dormant for years before causing total destruction.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Japan_Airlines_Flight_123",
            "tags": ["Maintenance", "Fatigue", "Shortcuts"]
        },

        # Finance (17-22)
        {
            "title": "Lehman Brothers Collapse",
            "domain": "Finance",
            "subdomain": "Investment Banking",
            "year": 2008,
            "organization": "Lehman Brothers",
            "what_failed": "The 158-year-old bank filed for the largest bankruptcy in US history ($600B), triggering the global financial crisis.",
            "root_cause": "Massive over-leveraging in toxic subprime mortgage-backed securities, combined with regulatory failure to enforce capital requirements.",
            "root_cause_category": "Incentive Misalignment",
            "warning_signs": [
                "Leverage ratio peaked at 31:1 (every $1 of equity backed $31 of debt)",
                "Internal risk teams were routinely ignored by executives",
                "Real estate market had been declining rapidly for over a year"
            ],
            "what_was_done_wrong": "Executives were paid massive bonuses for short-term gains while passing long-term catastrophic risk to the institution.",
            "how_it_was_fixed": "The firm was allowed to fail. Stricter banking regulations (Dodd-Frank) were passed globally.",
            "lesson": "If you reward short-term risk taking without accountability for long-term survival, the system will optimize for its own destruction.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Bankruptcy_of_Lehman_Brothers",
            "tags": ["Leverage", "Subprime", "Risk Management"]
        },
        {
            "title": "Long-Term Capital Management (LTCM)",
            "domain": "Finance",
            "subdomain": "Hedge Funds",
            "year": 1998,
            "organization": "LTCM",
            "what_failed": "A hedge fund led by Nobel Prize-winning economists collapsed, requiring a $3.6 billion bailout to prevent a global market crash.",
            "root_cause": "The firm's trading models assumed historical correlations would hold. When Russia defaulted on its debt, correlations broke down completely into a 'six-sigma' tail event.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "Models assumed absolute precision in inherently chaotic markets",
                "Fund was leveraged 25-to-1",
                "Ignored external macro-economic warnings regarding Russian debt"
            ],
            "what_was_done_wrong": "Blind faith in a mathematical model led to ignoring real-world contextual risk.",
            "how_it_was_fixed": "The US Federal Reserve orchestrated a bailout by 14 major banks to liquidate LTCM's assets orderly.",
            "lesson": "Genius fails when it forgets that models are approximations of reality, not reality itself.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Long-Term_Capital_Management",
            "tags": ["Models", "Leverage", "Tail Risk"]
        },
        {
            "title": "Bernie Madoff Ponzi Scheme",
            "domain": "Finance",
            "subdomain": "Wealth Management",
            "year": 2008,
            "organization": "Bernard L. Madoff Investment Securities",
            "what_failed": "The largest Ponzi scheme in history ($64 Billion) collapsed when too many investors attempted to withdraw funds during the financial crisis.",
            "root_cause": "A complete failure of regulatory oversight and due diligence, driven by Madoff's social prestige and artificially consistent returns.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Returns were impossibly smooth, lacking normal market volatility",
                "Whistleblower Harry Markopolos literally sent the SEC mathematical proof it was a fraud in 2005",
                "The firm's auditor was a tiny strip-mall accounting firm"
            ],
            "what_was_done_wrong": "Regulators and investors suspended disbelief because the returns were good. No one verified the actual trades.",
            "how_it_was_fixed": "Madoff sentenced to 150 years. SEC deeply reformed its investigative procedures.",
            "lesson": "If something seems too good to be true, and lacks transparency into its mechanics, it is a lie.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Madoff_investment_scandal",
            "tags": ["Fraud", "Regulation", "Trust Bias"]
        },
        {
            "title": "2010 Flash Crash",
            "domain": "Finance",
            "subdomain": "Algorithmic Trading",
            "year": 2010,
            "organization": "US Stock Market",
            "what_failed": "The Dow Jones index dropped 1,000 points (~$1 Trillion in value) in 5 minutes and rebounded 20 minutes later.",
            "root_cause": "A massive algorithmic sell order of E-Mini S&P contracts combined with aggressive spoofing by high-frequency traders drained market liquidity instantly.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "Market was already severely stressed from European debt crisis news",
                "High frequency trading algorithms had no logic to halt trading when liquidity vanished"
            ],
            "what_was_done_wrong": "Algorithms were coded to sell aggressively regardless of price or time, triggering a cascading chain reaction of automated panic selling.",
            "how_it_was_fixed": "The SEC implemented broader 'circuit breakers' that pause trading if stocks swing drastically in minutes.",
            "lesson": "Speed kills. Automated systems reacting to other automated systems will spiral out of control without built-in friction.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/2010_flash_crash",
            "tags": ["HFT", "Algorithms", "Circuit Breaker"]
        },
        {
            "title": "Silicon Valley Bank Run",
            "domain": "Finance",
            "subdomain": "Commercial Banking",
            "year": 2023,
            "organization": "Silicon Valley Bank",
            "what_failed": "SVB faced a $42 billion bank run in a single day, destroying the institution in 48 hours.",
            "root_cause": "The bank lacked a Chief Risk Officer for months and invested short-term deposits heavily into long-term bonds right before interest rates skyrocketed.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "93% of deposits were uninsured, meaning clients flight risk was massive",
                "Interest rate hikes were clearly signaled by the Fed for a year",
                "Venture capitalists publicly told their founders to pull money out"
            ],
            "what_was_done_wrong": "Failed to hedge interest rate risk. Failed to realize the speed at which a digital bank run spreads on Twitter.",
            "how_it_was_fixed": "FDIC took over the bank and guaranteed all deposits to stop systemic contagion.",
            "lesson": "In a connected world, trust evaporates at the speed of light. Unhedged mathematical risk becomes existential risk.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Collapse_of_Silicon_Valley_Bank",
            "tags": ["Interest Rates", "Bank Run", "Risk Management"]
        },
        {
            "title": "Barings Bank Rogue Trader",
            "domain": "Finance",
            "subdomain": "Investment Banking",
            "year": 1995,
            "organization": "Barings Bank",
            "what_failed": "The 233-year-old merchant bank was rendered insolvent after a single trader lost $1.3 billion in unauthorized derivatives trading.",
            "root_cause": "Nick Leeson held both the head of trading and head of settlement positions (back office), allowing him to hide losses in a secret error account (88888).",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Internal audits recommended splitting the roles a year prior",
                "Leeson requested massive margin funding from London without explaining the positions clearly",
                "Returns looked too good for arbitrage trading"
            ],
            "what_was_done_wrong": "London executives trusted Leeson unconditionally because he appeared highly profitable, turning a blind eye to missing controls.",
            "how_it_was_fixed": "The bank was sold for £1. The incident forced strict separation of front and back office duties banking-wide.",
            "lesson": "Never allow the person making the money to be the person checking the books. Separation of duties is mandatory.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Collapse_of_Barings_Bank",
            "tags": ["Rogue Trader", "Auditing", "Separation of Duties"]
        },

        # Healthcare (23-28)
        {
            "title": "Therac-25 Radiation Overdoses",
            "domain": "Healthcare",
            "subdomain": "Medical Devices",
            "year": 1985,
            "organization": "Atomic Energy of Canada Limited",
            "what_failed": "A software bug in a radiation therapy machine gave patients 100x the intended dose of radiation, killing at least 3 people.",
            "root_cause": "A race condition in the software existed. If an operator typed commands too quickly, the system deployed the high-power beam without the metal target shield in place.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "Machine displayed cryptic 'Malfunction 54' error codes",
                "Patients reported feeling a burning sensation",
                "Manufacturer denied the software could possibly fail"
            ],
            "what_was_done_wrong": "Hardware safety interlocks were removed to save costs, relying entirely on poorly-tested concurrent software.",
            "how_it_was_fixed": "Hardware safety interlocks were aggressively mandated for all medical radiating devices.",
            "lesson": "Never rely purely on software for life-critical safety. Always use physical hardware interlocks.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Therac-25",
            "tags": ["Software", "Race Condition", "Interlocks", "Denial"]
        },
        {
            "title": "Healthcare.gov Launch",
            "domain": "Healthcare",
            "subdomain": "Government IT",
            "year": 2013,
            "organization": "US Federal Government",
            "what_failed": "The $800M flagship health insurance portal crashed immediately on day 1. Only 6 people managed to enroll on the first day.",
            "root_cause": "Extreme fragmentation in contractors, lack of integration testing until 2 weeks before launch, and vastly underestimated database load.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Testing showed the site crashing at 200 users, but millions were expected",
                "Political pressure forced a hard launch date despite incomplete code",
                "No single project manager owned the full end-to-end architecture"
            ],
            "what_was_done_wrong": "Ignored load testing data entirely due to political pressure. Built a massive monolithic database block for authentication.",
            "how_it_was_fixed": "A specialized 'Trauma Team' of Silicon Valley engineers was flown in to rewrite caching rules and hardware configurations over 6 weeks.",
            "lesson": "You cannot bend the laws of computing to meet political deadlines. Integration testing must start on day one.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/HealthCare.gov",
            "tags": ["Launch", "Testing", "Load", "Contractors"]
        },
        {
            "title": "Vioxx Drug Withdrawal",
            "domain": "Healthcare",
            "subdomain": "Pharmaceuticals",
            "year": 2004,
            "organization": "Merck",
            "what_failed": "A blockbuster painkiller was pulled from the market after causing an estimated 88,000 to 140,000 cases of serious heart disease.",
            "root_cause": "Merck heavily promoted the drug while actively downplaying internal studies linking the drug to cardiovascular events.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "Early clinical trials showed increased cardiovascular risks",
                "Internal emails revealed doctors were instructed to dodge questions about heart issues",
                "FDA scientist sounded the alarm but was ignored"
            ],
            "what_was_done_wrong": "Prioritized immense quarterly profits over patient safety data, manipulating statistical outcomes in published papers.",
            "how_it_was_fixed": "Drug withdrawn globally. Merck paid $4.85 billion to settle lawsuits.",
            "lesson": "Data manipulation will eventually be caught by reality. The cost of ignoring safety signals is catastrophic.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Rofecoxib",
            "tags": ["Pharmaceuticals", "Ethics", "Data Manipulation"]
        },
        {
            "title": "Theranos Fraud",
            "domain": "Healthcare",
            "subdomain": "Medical Testing",
            "year": 2015,
            "organization": "Theranos",
            "what_failed": "A $9 billion blood-testing startup collapsed after it was revealed their core 'Edison' technology fundamentally didn't work and they were faking results.",
            "root_cause": "A culture of extreme secrecy, Silicon Valley 'fake it till you make it' mindset applied to healthcare, and punishing whistleblowers.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "Turnover in the technical lab was astronomically high",
                "The device consistently failed internal QC checks",
                "Scientists were siloed and forbidden from communicating with each other"
            ],
            "what_was_done_wrong": "Lied to investors, patients, and regulators. Used commercial third-party machines instead of their own to run tests.",
            "how_it_was_fixed": "Company dissolved. Founder Elizabeth Holmes sentenced to prison.",
            "lesson": "You cannot 'fake it till you make it' when dealing with biology and human life; physics and biology do not negotiate.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Theranos",
            "tags": ["Fraud", "Silicon Valley", "Secrecy"]
        },
        {
            "title": "UK NHS Lorenzo IT System",
            "domain": "Healthcare",
            "subdomain": "Enterprise Software",
            "year": 2011,
            "organization": "UK National Health Service",
            "what_failed": "A £10 billion attempt to create the world's largest centralized electronic health record system was scrapped as a total failure.",
            "root_cause": "Top-down government contract mandates forced commercial software onto diverse hospitals without consulting front-line doctors on usability.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Doctors outright refused to use the software because it increased their workload",
                "Continual scope creep changed requirements monthly",
                "Vendors routinely missed deployment deadlines"
            ],
            "what_was_done_wrong": "Ignored the end-user (clinicians). Built a monolithic solution for a decentralized problem.",
            "how_it_was_fixed": "Project cancelled. The NHS pivoted to localized systems with interoperability standards instead.",
            "lesson": "Never build massive software systems without sitting next to the people who will actually type the keys every day.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/NHS_Connecting_for_Health",
            "tags": ["Government IT", "Requirements", "End-Users"]
        },
        {
            "title": "Thalidomide Tragedy",
            "domain": "Healthcare",
            "subdomain": "Pharmaceuticals",
            "year": 1961,
            "organization": "Chemie Grünenthal",
            "what_failed": "A drug marketed for morning sickness caused over 10,000 severe birth defects worldwide.",
            "root_cause": "Lack of drug testing regulations. The drug was never tested on pregnant animals before being sold to pregnant human women.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Reports of peripheral neuritis in adults taking the drug",
                "Doctors began reporting sudden spikes in phocomelia (limb malformation)",
                "The company ignored complaints and continued to push sales"
            ],
            "what_was_done_wrong": "Released an untested chemical isomer into the market targeting a vulnerable demographic.",
            "how_it_was_fixed": "Drug banned globally. Led to the creation of strict, modern FDA drug trial phases.",
            "lesson": "Absence of evidence of harm is not evidence of safety. Rigorous testing is mandatory.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Thalidomide_scandal",
            "tags": ["Testing", "Regulation", "Birth Defects"]
        },
        
        # Space (29-34)
        {
            "title": "Challenger Space Shuttle Launch",
            "domain": "Space",
            "subdomain": "Manned Spaceflight",
            "year": 1986,
            "organization": "NASA",
            "what_failed": "The Space Shuttle broke apart 73 seconds into flight, killing all 7 crew members.",
            "root_cause": "O-ring seals in the solid rocket booster hardened in freezing launch temperatures, allowing hot gas to blowtorch the external fuel tank.",
            "root_cause_category": "Ignored Warning Signs",
            "warning_signs": [
                "Engineers explicitly warned management the night before that launching below 53°F was unsafe",
                "Previous launches showed partial O-ring erosion (normalized deviance)",
                "Ice was clearly visible on the launch pad"
            ],
            "what_was_done_wrong": "NASA management succumbed to schedule pressure and PR pressure. They asked engineers to 'take off your engineering hat and put on your management hat.'",
            "how_it_was_fixed": "Redesigned booster joints with multiple redundancies. NASA cultural overhaul.",
            "lesson": "You cannot out-manage physics. When engineers tell you a system will fail, listen to them.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Space_Shuttle_Challenger_disaster",
            "tags": ["Culture", "Normalization of Deviance", "O-rings"]
        },
        {
            "title": "Columbia Space Shuttle Re-entry",
            "domain": "Space",
            "subdomain": "Manned Spaceflight",
            "year": 2003,
            "organization": "NASA",
            "what_failed": "The Space Shuttle disintegrated upon re-entry into Earth's atmosphere, killing 7 crew members.",
            "root_cause": "A piece of foam insulation broke off during launch and struck the leading edge of the left wing, punching a hole in the heat shield.",
            "root_cause_category": "Ignored Warning Signs",
            "warning_signs": [
                "Foam striking the shuttle was a known issue on almost every prior flight",
                "Engineers requested DoD spy satellite imaging of the wing mid-flight but the request was denied by management"
            ],
            "what_was_done_wrong": "Management classified foam strikes as a 'maintenance issue' rather than a 'safety of flight' issue. Normalization of deviance struck again.",
            "how_it_was_fixed": "Shuttle fleet grounded. Heat shield inspection via robotic arm mandated for all future flights.",
            "lesson": "Just because an anomaly hasn't killed you yet doesn't mean it is safe. Red flags don't become green just because you survive them once.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Space_Shuttle_Columbia_disaster",
            "tags": ["Culture", "Normalization of Deviance", "Foam"]
        },
        {
            "title": "Mars Climate Orbiter",
            "domain": "Space",
            "subdomain": "Robotic Probes",
            "year": 1999,
            "organization": "NASA / Lockheed Martin",
            "what_failed": "A $193 million spacecraft disintegrated in the Martian atmosphere because it navigated too close to the planet.",
            "root_cause": "A mismatch in unit systems. The Lockheed software supplied thruster data in imperial units (pound-seconds), while NASA software expected metric units (newton-seconds).",
            "root_cause_category": "Communication Breakdown",
            "warning_signs": [
                "Navigators noticed discrepancies in trajectory data for months during transit",
                "Concerns were swept aside as 'normal noise' rather than investigated"
            ],
            "what_was_done_wrong": "Lack of end-to-end interface testing. Failure to verify interface documentation between two contracting organizations.",
            "how_it_was_fixed": "NASA required all projects to use the metric system universally.",
            "lesson": "Interface contracts are absolute. Assumptions across team boundaries must be explicitly validated in code.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Mars_Climate_Orbiter",
            "tags": ["Units", "Interface", "Integration Testing"]
        },
        {
            "title": "Ariane 5 Flight 501",
            "domain": "Space",
            "subdomain": "Launch Vehicles",
            "year": 1996,
            "organization": "European Space Agency",
            "what_failed": "The rocket veered off course and exploded 37 seconds after launch, destroying a $500 million satellite payload.",
            "root_cause": "An integer overflow. An attempt to convert a 64-bit floating-point number into a 16-bit signed integer caused a hardware exception.",
            "root_cause_category": "Technical Debt",
            "warning_signs": [
                "The code was copied directly from Ariane 4, which had lower velocity profiles",
                "The exception handling for that specific block had been turned off to save CPU cycles"
            ],
            "what_was_done_wrong": "Software reuse without re-validating the operational bounds of the new hardware environment.",
            "how_it_was_fixed": "Added bounds checking to variables and ran comprehensive simulation testbeds for future launches.",
            "lesson": "Code that works perfectly in one environment is toxic in another. Never reuse code without validating the new constraints.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Ariane_flight_V88",
            "tags": ["Software", "Overflow", "Code Reuse"]
        },
        {
            "title": "Apollo 1 Fire",
            "domain": "Space",
            "subdomain": "Manned Spaceflight",
            "year": 1967,
            "organization": "NASA",
            "what_failed": "A cabin fire during a launch pad test killed three astronauts.",
            "root_cause": "A spark in faulty wiring ignited combustible materials due to the highly pressurized 100% pure oxygen environment in the cabin.",
            "root_cause_category": "Single Point of Failure",
            "warning_signs": [
                "Extensive use of flammable Velcro throughout the cabin",
                "Astronauts complained about communication glitches and a 'sour milk' smell before the fire",
                "The inward-opening hatch took over 90 seconds to open under pressure"
            ],
            "what_was_done_wrong": "Ignored the extreme flammability risk of pure oxygen at high pressure. Designed a complex escape hatch.",
            "how_it_was_fixed": "Switched to a mixed oxygen/nitrogen atmosphere on pad. Redesigned hatch to open outwards in 3 seconds.",
            "lesson": "Don't compound risks. If using a dangerous baseline (pure oxygen), all other physical risks must be minimized to zero.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Apollo_1",
            "tags": ["Design", "Fire Risk", "Testing"]
        },
        {
            "title": "Hubble Space Telescope Mirror",
            "domain": "Space",
            "subdomain": "Telescopes",
            "year": 1990,
            "organization": "NASA / Perkin-Elmer",
            "what_failed": "The multi-billion dollar telescope reached orbit only for scientists to realize its primary mirror was ground to the wrong shape, causing blurry images.",
            "root_cause": "A physical measurement device (null corrector) was assembled incorrectly by 1.3 millimeters. No independent cross-check test was performed.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "A secondary, simpler testing device actually indicated the mirror was wrong, but it was ignored because the primary device was considered 'more precise'",
                "The contractor was vastly behind schedule and over budget"
            ],
            "what_was_done_wrong": "Relianced on a single point of truth for measurement without an independent validation test.",
            "how_it_was_fixed": "Astronauts had to install corrective optics (COSTAR) during a dangerous spacewalk 3 years later.",
            "lesson": "Always have an independent, geometrically different way to verify your most critical system parameters.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Hubble_Space_Telescope",
            "tags": ["Testing", "Quality Assurance", "Optics"]
        },

        # Government/Infrastructure (35-40)
        {
            "title": "Chernobyl Nuclear Disaster",
            "domain": "Government",
            "subdomain": "Nuclear Power",
            "year": 1986,
            "organization": "Soviet Union",
            "what_failed": "Reactor No. 4 exploded, releasing massive radioactive contamination and rendering the area uninhabitable.",
            "root_cause": "A fundamentally flawed reactor design (RBMK positive void coefficient) combined with a night crew pushing the reactor outside safe operating limits for a test.",
            "root_cause_category": "Ignored Warning Signs",
            "warning_signs": [
                "The reactor had 'poisoned out' with Xenon, dropping power far below the test baseline",
                "Operating manuals forbid disabling safety systems, which the crew did anyway",
                "Engineers knew about the graphite tip design flaw but kept it state secret"
            ],
            "what_was_done_wrong": "Pushed forward with a delayed test under unstable conditions due to bureaucratic pressure. Activated the fail-safe (AZ-5) which ironically triggered the explosion.",
            "how_it_was_fixed": "Sarcophagus built over reactor. RBMK designs worldwide were retrofitted.",
            "lesson": "Authoritarian systems that punish bad news ensure that catastrophic flaws remain hidden until they explode.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Chernobyl_disaster",
            "tags": ["Nuclear", "Culture", "Design Flaw"]
        },
        {
            "title": "Deepwater Horizon Oil Spill",
            "domain": "Infrastructure",
            "subdomain": "Energy Drilling",
            "year": 2010,
            "organization": "BP / Transocean",
            "what_failed": "A blowout off the coast of Louisiana destroyed the rig, killed 11 workers, and dumped 210 million gallons of oil into the Gulf.",
            "root_cause": "Cement casing failed to contain high-pressure gas, and the Blowout Preventer (BOP) blind shear rams failed to cut the drill pipe.",
            "root_cause_category": "Technical Debt", # Also cost-cutting / incentive misalignment
            "warning_signs": [
                "Pressure tests on the cement plug showed wildly abnormal readings",
                "The rig was 43 days behind schedule, costing $1 million a day, driving rushed decisions",
                "Workers dismissed pressure anomalies as 'bladder effect'"
            ],
            "what_was_done_wrong": "Ignored negative pressure tests. Bypassed safety barriers to speed up the temporary abandonment of the well.",
            "how_it_was_fixed": "Well capped after 87 days. BP paid $65 Billion in fines and cleanup costs.",
            "lesson": "When schedule pressure dictates safety decisions, the system will eventually optimize for a catastrophe.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Deepwater_Horizon_oil_spill",
            "tags": ["Oil", "Cost-Cutting", "Pressure"]
        },
        {
            "title": "Tacoma Narrows Bridge Collapse",
            "domain": "Infrastructure",
            "subdomain": "Civil Engineering",
            "year": 1940,
            "organization": "Washington State",
            "what_failed": "A suspension bridge tore itself apart in 40 mph winds due to aeroelastic flutter.",
            "root_cause": "The bridge was designed with solid girders instead of open trusses, catching the wind. Engineers did not account for aerodynamic resonance forces.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "Construction workers noted the bridge bounced severely during building",
                "Locals nicknamed it 'Galloping Gertie' months before collapse due to its rolling motion"
            ],
            "what_was_done_wrong": "Focused purely on static load modeling (weight, tension) rather than dynamic environmental factors (wind patterns).",
            "how_it_was_fixed": "Rebuilt with deep, open steel stiffening trusses. Gave birth to modern bridge aerodynamics engineering.",
            "lesson": "Models that ignore environmental dynamics are incomplete. Systems exist within an active environment, not a vacuum.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)",
            "tags": ["Resonance", "Wind", "Design"]
        },
        {
            "title": "New Orleans Levees (Katrina)",
            "domain": "Infrastructure",
            "subdomain": "Flood Control",
            "year": 2005,
            "organization": "US Army Corps of Engineers",
            "what_failed": "The floodwall system protecting New Orleans catastrophically failed during Hurricane Katrina, overflowing 80% of the city.",
            "root_cause": "Levee foundations were dug far too shallow in soft soil to save money, causing them to slide horizontally when water pressure rose.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Numerous engineering models predicted failure in a Category 3+ storm",
                "Funding had been repeatedly slashed for maintenance and upgrades",
                "Evacuation protocols largely ignored the socio-economic reality of car-less residents"
            ],
            "what_was_done_wrong": "Used outdated data for soil mechanics. Relied on a fragmented system of local levee boards with vague accountability.",
            "how_it_was_fixed": "System rebuilt over 10 years at a cost of $14.5 Billion with much deeper pilings and automated surge barriers.",
            "lesson": "You cannot negotiate with water pressure. Infrastructure built to the bare minimum standard will yield maximum destruction.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Levee_failures_in_Greater_New_Orleans,_2005",
            "tags": ["Infrastructure", "Soil", "Underfunding"]
        },
        {
            "title": "Texas Power Grid Failure",
            "domain": "Infrastructure",
            "subdomain": "Power Grid",
            "year": 2021,
            "organization": "ERCOT",
            "what_failed": "A severe winter storm caused widespread failure of the Texas power grid, leaving millions freezing for days.",
            "root_cause": "Power generators (natural gas, coal, wind) were not winterized. Natural gas wellheads froze, cutting fuel to the power plants precisely when demand spiked.",
            "root_cause_category": "Incentive Misalignment",
            "warning_signs": [
                "A perfectly identical freeze caused outages in 2011, prompting federal reports to beg Texas to winterize",
                "The deregulated market only paid for electricity *generated*, not capacity *reserved*"
            ],
            "what_was_done_wrong": "Ignored 2011 warnings because winterizing equipment was expensive and not legally required. Grid managers were moments away from total unrecoverable grid meltdown.",
            "how_it_was_fixed": "Legislation passed requiring winterization, though critics say enforcement loopholes remain.",
            "lesson": "If resilience is not financially incentivized or legally mandated in a free market, it will not exist.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/2021_Texas_power_crisis",
            "tags": ["Grid", "Deregulation", "Weather"]
        },
        {
            "title": "FBI Virtual Case File",
            "domain": "Government",
            "subdomain": "Government IT",
            "year": 2005,
            "organization": "FBI",
            "what_failed": "The FBI scrapped a completed $170 million software system meant to modernize counter-terrorism databases after 9/11.",
            "root_cause": "Attempted an arrogant 'big bang' complete rewrite of the entire FBI software ecosystem without a stable requirements document.",
            "root_cause_category": "Over-Complexity",
            "warning_signs": [
                "700+ pages of requirements were drafted, but modified constantly during coding",
                "High turnover: 5 different CIOs in 4 years",
                "Contractors delivered 700,000 lines of code with massive architectural flaws"
            ],
            "what_was_done_wrong": "Failed to use iterative development. Built a monolith from scratch based on vague enterprise architecture rules.",
            "how_it_was_fixed": "System cancelled completely. FBI successfully rebuilt using an agile, modular approach (Sentinel project).",
            "lesson": "Never do a 'big bang' rewrite. Evolve large systems slowly, iteratively, and with constant user feedback.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Virtual_Case_File",
            "tags": ["IT", "Agile", "Scope Creep"]
        },

        # Cybersecurity / Other Requested (41-48)
        {
            "title": "Heartbleed Vulnerability",
            "domain": "Cybersecurity",
            "subdomain": "Open Source",
            "year": 2014,
            "organization": "OpenSSL",
            "what_failed": "A bug in the widely used OpenSSL cryptography library allowed attackers to read the memory of servers, exposing passwords and private keys globally.",
            "root_cause": "A missing bounds check in the handling of the TLS 'heartbeat' extension allowed a client to request up to 64KB of server memory.",
            "root_cause_category": "Technical Debt",
            "warning_signs": [
                "OpenSSL was vastly underfunded, managed by only 2 guys, despite securing millions of web servers",
                "The codebase was notoriously archaic and hard to read"
            ],
            "what_was_done_wrong": "The tech industry extracted immense value from a critical piece of open-source software without contributing to its security audits or maintenance.",
            "how_it_was_fixed": "A patch was rushed out. Massive tech companies formed the Core Infrastructure Initiative to fund critical open-source projects.",
            "lesson": "Your multi-billion-dollar corporation's security relies on the unpaid labor of people you don't know over the internet. Fund open source.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Heartbleed",
            "tags": ["Open Source", "C/C++", "Memory bounds"]
        },
        {
            "title": "Log4Shell",
            "domain": "Cybersecurity",
            "subdomain": "Open Source",
            "year": 2021,
            "organization": "Apache Software Foundation",
            "what_failed": "A zero-day vulnerability in Log4j allowed unauthenticated remote code execution (RCE) on billions of Java applications.",
            "root_cause": "A legacy feature (JNDI lookup) was enabled by default, allowing the logger to execute code downloaded from a malicious string merely by logging it.",
            "root_cause_category": "External Dependency Failure",
            "warning_signs": [
                "Feature was added years prior for a specific edge case but left on globally",
                "Engineers rarely reviewed deep dependency trees of their logging tools"
            ],
            "what_was_done_wrong": "Building complex active execution capabilities into what should just be a dumb text-writing utility.",
            "how_it_was_fixed": "A massive, chaotic global scramble to patch servers in December 2021. JNDI lookups were disabled by default.",
            "lesson": "Dependencies are hidden liabilities. Features you didn't ask for in libraries you didn't evaluate can destroy your company.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Log4Shell",
            "tags": ["Dependencies", "Java", "RCE"]
        },
        {
            "title": "Equifax Data Breach",
            "domain": "Cybersecurity",
            "subdomain": "Data Privacy",
            "year": 2017,
            "organization": "Equifax",
            "what_failed": "Hackers stole personal data (SSNs) of 147 million Americans via a vulnerability in a web portal.",
            "root_cause": "Equifax failed to apply a known Apache Struts security patch that was released two months prior to the breach.",
            "root_cause_category": "Security Negligence",
            "warning_signs": [
                "The patch was publicly known and heavily documented",
                "Equifax had massive technical debt and disorganized network segmentation",
                "Passwords were stored in plain text internally"
            ],
            "what_was_done_wrong": "Total failure of fundamental IT hygiene. The security scan meant to find unpatched servers missed the vulnerable machine.",
            "how_it_was_fixed": "Equifax paid $700+ million in settlements. Key executives were fired or indicted.",
            "lesson": "There is no advanced hacker magic required if you leave the front door unlocked for two months.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/2017_Equifax_data_breach",
            "tags": ["Patching", "Data Breach", "IT Hygiene"]
        },
        {
            "title": "Enron Accounting Fraud",
            "domain": "Finance",
            "subdomain": "Energy Trading",
            "year": 2001,
            "organization": "Enron",
            "what_failed": "The 7th largest US company imploded in weeks when it was revealed their massive profits were entirely fictional accounting tricks.",
            "root_cause": "Mark-to-market accounting allowed claiming future estimated profits today. Hideous losses were shoved into 'Special Purpose Entities' off the balance sheet.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "Executives vigorously crushed internal disagreement",
                "Cash flow from operations never matched the reported earnings",
                "Arthur Andersen auditors were compromised due to consulting fees"
            ],
            "what_was_done_wrong": "Leadership created a toxic 'rank and yank' culture where employees competed ruthlessly, incentivizing fraud. Auditors blessed the fraud.",
            "how_it_was_fixed": "Company bankrupt. Sarbanes-Oxley Act passed to hold CEOs personally liable for financial reporting.",
            "lesson": "A toxic culture of hyper-competition combined with opaque metrics will invariably turn honest employees into criminals.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Enron_scandal",
            "tags": ["Fraud", "Culture", "Accounting"]
        },
        {
            "title": "MySpace Subsumed by Facebook",
            "domain": "Software Engineering",
            "subdomain": "Social Media",
            "year": 2008,
            "organization": "MySpace",
            "what_failed": "The dominant social network lost basically all of its user base to Facebook in a short span of time.",
            "root_cause": "Spaghetti code architecture meant releasing new features took months, while user-generated custom CSS ruined page load speeds and usability.",
            "root_cause_category": "Technical Debt",
            "warning_signs": [
                "Pages were filled with flashing text, auto-playing music, and horrific layouts",
                "Facebook offered a clean, structured, predictably fast alternative",
                "MySpace was built entirely defensively after Fox acquisition, trying to extract ad value"
            ],
            "what_was_done_wrong": "Valued extreme user customizability over user experience and performance infrastructure.",
            "how_it_was_fixed": "Sold for pennies. Facebook became a monopoly.",
            "lesson": "If your inner technical architecture is chaotic, it will eventually manifest as a chaotic and broken user experience.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Myspace",
            "tags": ["UX", "Technical Debt", "Product Management"]
        },
        {
            "title": "Kodak Missing the Digital Revolution",
            "domain": "Manufacturing",
            "subdomain": "Consumer Electronics",
            "year": 2012,
            "organization": "Kodak",
            "what_failed": "The company that literally invented the digital camera filed for bankruptcy because it refused to pivot away from film.",
            "root_cause": "Cognitive entrenchment. Executives saw Kodak as a 'chemicals and paper' company, fearing digital would cannibalize their highly profitable film sales.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "In-house engineers built a digital prototype in 1975, but management shelved it",
                "Sales of traditional film sharply dropped while digital curves rose exactly as internal analysts predicted in 1981"
            ],
            "what_was_done_wrong": "Management chose to milk the dying cash cow rather than innovate. They viewed digital as a tool to print more photos, missing social sharing altogether.",
            "how_it_was_fixed": "Bankrupt. Sold off vast patent portfolios to survive as a niche printing company.",
            "lesson": "If you do not cannibalize your own product, somebody else will do it for you.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Kodak",
            "tags": ["Innovation", "Cannibalization", "Strategy"]
        },
        {
            "title": "BlackBerry's Decline",
            "domain": "Manufacturing",
            "subdomain": "Mobile Space",
            "year": 2010,
            "organization": "Research In Motion (RIM)",
            "what_failed": "The dominant smartphone maker lost 90%+ market share to Apple hardware and Android software.",
            "root_cause": "RIM believed consumers primarily wanted secure email and physical keyboards, dismissing the iPhone as a battery-draining toy.",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "Consumers wanted apps and media, not enterprise security",
                "Developers flocked to the iPhone because the App Store was infinitely easier to develop for than BlackBerry OS"
            ],
            "what_was_done_wrong": "Prioritized carriers and IT managers over end-consumer sentiment. Attempted half-measures like the Storm rather than fully committing to touch.",
            "how_it_was_fixed": "Shifted entirely to enterprise software. No longer builds phones.",
            "lesson": "Past success breeds absolute blindness to paradigm shifts. Listen to the market, not your legacy customer base.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/BlackBerry_(company)",
            "tags": ["Strategy", "Disruption", "Denial"]
        },

        # Military (48-52)
        {
            "title": "Pearl Harbor Surprise Attack",
            "domain": "Military",
            "subdomain": "Intelligence",
            "year": 1941,
            "organization": "US Navy",
            "what_failed": "The US Pacific Fleet was devastated by a surprise Japanese air attack despite multiple intelligence warnings.",
            "root_cause": "Siloed intelligence agencies refused to share data, and commanders suffered cognitive bias, believing Pearl Harbor was too shallow for torpedo attacks.",
            "root_cause_category": "Communication Breakdown",
            "warning_signs": [
                "Radar operators saw incoming planes but were told 'Don't worry about it, it's incoming B-17s'",
                "A Japanese mini-submarine was sunk outside the harbor hours before the attack",
                "Cryptanalysts intercepted messages indicating war was imminent"
            ],
            "what_was_done_wrong": "Fragmented intelligence flow meant no single person saw the complete picture. The system was tuned for a sabotage threat, not an air attack.",
            "how_it_was_fixed": "Led to the complete restructuring of US Intelligence and the creation of the CIA.",
            "lesson": "Information silos kill. If data isn't correlated and shared across the enterprise, it is useless.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Attack_on_Pearl_Harbor",
            "tags": ["Intelligence", "Silos", "Cognitive Bias"]
        },
        {
            "title": "Patriot Missile Failure at Dhahran",
            "domain": "Military",
            "subdomain": "Software Engineering",
            "year": 1991,
            "organization": "US Army",
            "what_failed": "An Iraqi Scud missile hit US barracks in Saudi Arabia, killing 28 soldiers, because the interception system failed to track it.",
            "root_cause": "A software rounding error in calculating time. The battery was left on for 100 hours, causing a time calculation drift of 0.34 seconds, meaning the radar looked in the wrong place.",
            "root_cause_category": "Technical Debt",
            "warning_signs": [
                "The system was designed for Soviet planes, assuming it would be moved/reset frequently, not left on constantly",
                "Israel noticed the drift weeks prior and warned the US Army"
            ],
            "what_was_done_wrong": "Used a 24-bit register for a precision floating point calculation, resulting in cumulative loss of precision over uptime.",
            "how_it_was_fixed": "Software patch arrived the day after the attack. Rebooting procedures were strictly regimented.",
            "lesson": "Small inaccuracies compound exponentially over time. Understand the original assumptions a system was built upon.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/MIM-104_Patriot",
            "tags": ["Floating Point", "System Uptime", "Math"]
        },
        {
            "title": "USS Vincennes shoots down Iran Air 655",
            "domain": "Military",
            "subdomain": "Naval Warfare",
            "year": 1988,
            "organization": "US Navy",
            "what_failed": "An Aegis cruiser shot down a civilian airliner over the Persian Gulf, killing 290 people.",
            "root_cause": "The radar UI in the Combat Information Center was horribly confusing, leading operators to misidentify the climbing Airbus as a descending F-14 fighter jet.",
            "root_cause_category": "Human Error",
            "warning_signs": [
                "The Aegis system actually had the correct altitude data, but it was presented in a confusing way",
                "Operators were under extreme psychological stress from a surface skirmish moments prior"
            ],
            "what_was_done_wrong": "Designed a UI that presented raw data rather than actionable insight under pressure. Scenario fulfillment bias took over the crew.",
            "how_it_was_fixed": "Massive overhaul of the Aegis interface and human-computer interaction studies in military design.",
            "lesson": "User interface design under stress is life or death. Do not make users perform complex mental math in a crisis.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Iran_Air_Flight_655",
            "tags": ["UI/UX", "Stress", "Cognitive Bias"]
        },
        {
            "title": "Maginot Line Bypassed",
            "domain": "Military",
            "subdomain": "Defense Strategy",
            "year": 1940,
            "organization": "French Army",
            "what_failed": "France's impenetrable, multi-billion franc defensive fortification line was rendered useless when Germany simply went around it through the Ardennes forest.",
            "root_cause": "French generals prepared perfectly to fight the previous war (WWI static trenches) ignoring the speed and mechanical nature of the new war (Blitzkrieg).",
            "root_cause_category": "Leadership Failure",
            "warning_signs": [
                "German Panzer units were explicitly designed for speed and maneuverability",
                "Aviation had advanced to easily bypass static ground fortifications"
            ],
            "what_was_done_wrong": "Assumed the dense Ardennes forest was 'impassable' to tanks without actual testing. Placed all resources into a static asset.",
            "how_it_was_fixed": "France fell in 6 weeks.",
            "lesson": "Do not optimize perfectly for a threat that no longer exists.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Maginot_Line",
            "tags": ["Strategy", "Adaptability", "Static Defense"]
        },
        
        # Additional Diverse Failures to hit 60 (53-60)
        {
            "title": "Fukushima Daiichi Disaster",
            "domain": "Government",
            "subdomain": "Energy Infrastructure",
            "year": 2011,
            "organization": "TEPCO",
            "what_failed": "Three nuclear meltdowns occurred after a tsunami knocked out backup generators.",
            "root_cause": "Backup diesel generators were placed in basements, vulnerable to flooding, despite historical evidence of massive tsunamis in the region.",
            "root_cause_category": "Ignored Warning Signs",
            "warning_signs": [
                "Seismologists explicitly warned TEPCO years earlier that a 10+ meter tsunami was historically possible",
                "The seawall was only built to withstand a 5.7 meter wave"
            ],
            "what_was_done_wrong": "Arrogant belief in geological stability and reluctance to spend money upgrading seawalls. Failure to imagine compounding black-swan events.",
            "how_it_was_fixed": "Generators moved to high ground globally. Redundant battery systems installed.",
            "lesson": "When modeling disaster, assume the worst possible scenario, then assume your primary defense fails.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Fukushima_nuclear_disaster",
            "tags": ["Tsunami", "Nuclear", "Risk Planning"]
        },
        {
            "title": "Samsung Galaxy Note 7 Fires",
            "domain": "Manufacturing",
            "subdomain": "Consumer Electronics",
            "year": 2016,
            "organization": "Samsung",
            "what_failed": "Flagship smartphones began spontaneously combusting globally, leading to a total recall and ban from all airlines.",
            "root_cause": "Extreme design pressure to pack an enormous battery into a tiny, curved ultra-thin chassis meant the battery had zero physical room to expand dynamically during charging.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Rushed manufacturing timelines to beat the iPhone 7 release",
                "First wave of 'fixed' replacement phones also caught fire due to a separate manufacturer flaw"
            ],
            "what_was_done_wrong": "Prioritized aesthetic design over physical engineering tolerances.",
            "how_it_was_fixed": "Multi-billion dollar recall. Implemented an 8-point strict battery safety check.",
            "lesson": "Physics is the ultimate edge case. If you remove the margin for error, errors become explosive.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Samsung_Galaxy_Note_7",
            "tags": ["Hardware", "Battery", "Design Pressure"]
        },
        {
            "title": "Target Data Breach",
            "domain": "Cybersecurity",
            "subdomain": "Retail IT",
            "year": 2013,
            "organization": "Target",
            "what_failed": "Hackers stole 40 million credit card numbers during the holiday shopping season.",
            "root_cause": "Hackers stole network credentials from an HVAC vendor, accessed the internal network, and deployed malware to the point-of-sale registers.",
            "root_cause_category": "Security Negligence",
            "warning_signs": [
                "Target's expensive FireEye security system actually caught the malware and fired alerts, but the security team in India and Minneapolis ignored them"
            ],
            "what_was_done_wrong": "Allowed a third-party vendor unrestricted access to the sensitive payment network. Alert fatigue caused them to ignore real warnings.",
            "how_it_was_fixed": "Segmented network architecture. Forced chip-and-pin (EMV) card adoption in the US.",
            "lesson": "Your security is only as strong as the weakest vendor you give VPN access to. Alert fatigue is a critical vulnerability.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Target_Corporation_data_breach",
            "tags": ["Third-Party", "Network Segmentation", "Alert Fatigue"]
        },
        {
            "title": "SolarWinds Hack (Sunburst)",
            "domain": "Cybersecurity",
            "subdomain": "Supply Chain",
            "year": 2020,
            "organization": "SolarWinds",
            "what_failed": "Russian state hackers breached SolarWinds and inserted a backdoor into their Orion software updates, compromising thousands of high-level US government agencies and Fortune 500 companies.",
            "root_cause": "Hackers compromised the build server pipeline itself. The compiled software was maliciously altered but perfectly digitally signed by SolarWinds.",
            "root_cause_category": "Security Negligence",
            "warning_signs": [
                "The company's update server password was widely reported to be 'solarwinds123' earlier",
                "Massive use of offshore engineering teams with poor credential rotations"
            ],
            "what_was_done_wrong": "Failed to secure the software build and release pipeline.",
            "how_it_was_fixed": "Massive incident response globally. Forced the concept of Software Bill of Materials (SBOM) into the mainstream.",
            "lesson": "An attacker doesn't need to break down the front door if they can poison the water supply.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/2020_United_States_federal_government_data_breach",
            "tags": ["Supply Chain", "Nation State", "Build Pipeline"]
        },
        {
            "title": "Ford Pinto Fuel Tanks",
            "domain": "Manufacturing",
            "subdomain": "Automotive",
            "year": 1970,
            "organization": "Ford",
            "what_failed": "The subcompact car repeatedly burst into flames during low-speed rear-end collisions.",
            "root_cause": "The fuel tank was placed behind the rear axle with brittle bolts that would puncture the tank. Ford decided fixing it ($11 per car) was more expensive than paying out wrongful death settlements.",
            "root_cause_category": "Incentive Misalignment",
            "warning_signs": [
                "Internal crash tests routinely showed catastrophic fuel leakage",
                "The infamous 'Pinto Memo' literally calculated the cost of human lives vs the cost of a plastic baffle"
            ],
            "what_was_done_wrong": "Management applied cold corporate calculus to severe safety risks, deciding deaths were 'acceptable' costs.",
            "how_it_was_fixed": "Recalled 1.5 million vehicles. Resulted in massive punitive damage lawsuit verdicts.",
            "lesson": "Do not treat human life as an acceptable loss on a spreadsheet. Society will destroy you.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Ford_Pinto",
            "tags": ["Ethics", "Cost-Benefit", "Design Defect"]
        },
        {
            "title": "NotPetya Ransomware Attack",
            "domain": "Cybersecurity",
            "subdomain": "Cyberwarfare",
            "year": 2017,
            "organization": "Global (Maersk, FedEx, etc)",
            "what_failed": "The most devastating cyberattack in history cost $10 billion globally in totally paralyzed logistics, shipping, and pharmaceutical systems.",
            "root_cause": "Russian hackers injected destructive worm into a Ukrainian tax software update. The worm spread laterally using the EternalBlue NSA exploit, wiping hard drives permanently.",
            "root_cause_category": "External Dependency Failure",
            "warning_signs": [
                "The EternalBlue exploit had been patched by Microsoft months earlier, but massive global enterprises hadn't installed the patch",
                "Companies had flat networks with zero segmentation"
            ],
            "what_was_done_wrong": "Relied on outdated flat network architectures. The malware didn't even ask for a real ransom; its only purpose was unrecoverable destruction.",
            "how_it_was_fixed": "Maersk had to rebuild 4,000 servers and 45,000 PCs from a single un-networked domain controller found in Ghana.",
            "lesson": "Patching is not optional, and flat networks are a death sentence during a worm outbreak.",
            "severity": "Critical",
            "source_url": "https://en.wikipedia.org/wiki/Petya_and_NotPetya",
            "tags": ["Ransomware", "Patching", "Supply Chain"]
        },
        {
            "title": "Boeing Starliner Software Anomalies",
            "domain": "Space",
            "subdomain": "Manned Spaceflight",
            "year": 2019,
            "organization": "Boeing",
            "what_failed": "The unmanned test capsule failed to reach the ISS because an internal clock was off by 11 hours, burning fuel at the wrong time.",
            "root_cause": "The spacecraft read the time from the Atlas V rocket incorrectly before launch, and a second bug would have destroyed the craft on re-entry if not patched mid-flight.",
            "root_cause_category": "Process Failure",
            "warning_signs": [
                "Boeing engineers broke the test up into thousands of sub-tests but never did a single complete end-to-end mission simulation",
                "Over-confidence in previous heritage code"
            ],
            "what_was_done_wrong": "Lack of end-to-end software integration testing. Testing hardware and software separately.",
            "how_it_was_fixed": "NASA mandated an entire second uncrewed flight test at Boeing's expense ($400M).",
            "lesson": "Unit tests do not guarantee integration success. Test the entire system together as it will fly.",
            "severity": "High",
            "source_url": "https://en.wikipedia.org/wiki/Boeing_Starliner",
            "tags": ["Software", "Integration Testing", "Clocks"]
        },
        {
            "title": "Equinox Fitness Data Exposure",
            "domain": "Software Engineering",
            "subdomain": "APIs",
            "year": 2024,
            "organization": "Equinox",
            "what_failed": "Health data and location history for millions of members were exposed via an insecure API Endpoint.",
            "root_cause": "An API was left completely unauthenticated, assuming 'security by obscurity' because the endpoint was only used internally by the mobile app.",
            "root_cause_category": "Security Negligence",
            "warning_signs": [
                "Endpoint required no token or session ID",
                "IDs were sequential integers (Insecure Direct Object Reference - IDOR)"
            ],
            "what_was_done_wrong": "Iterated through sequential user IDs on an open API to scrape the database.",
            "how_it_was_fixed": "Endpoint taken offline, authentication checks added to every route.",
            "lesson": "Security by obscurity never works on the internet. All APIs, internal or external, must authenticate and authorize.",
            "severity": "Medium",
            "source_url": "https://www.theverge.com/",
            "tags": ["API", "IDOR", "Authentication"]
        }
    ]
    
    # Returning exactly as requested
    return failures
