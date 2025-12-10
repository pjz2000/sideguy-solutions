import fs from "fs";



const pages = [

 const pages = [

  { slug: 'San-Diego-Payment-Processing.html', title: 'San Diego Payment Processing' },

  { slug: 'San-Diego-Instant-Settlements.html', title: 'San Diego Instant Settlements' },

  { slug: 'San-Diego-Lower-Credit-Card-Fees.html', title: 'San Diego Lower Credit Card Fees' },

  { slug: 'North-County-Payment-Processing.html', title: 'North County Payment Processing' },

  { slug: 'North-County-Instant-Settlements.html', title: 'North County Instant Settlements' },

  { slug: 'North-County-Solana-Payments.html', title: 'North County Solana Payments' },

  { slug: 'Carlsbad-Contractor-Payments.html', title: 'Carlsbad Contractor Payments' },

  { slug: 'Carlsbad-Lower-Credit-Card-Fees.html', title: 'Carlsbad Lower Credit Card Fees' },

  { slug: 'Cardiff-Payment-Processing.html', title: 'Cardiff Payment Processing' },

  { slug: 'Del-Mar-Lower-Credit-Card-Fees.html', title: 'Del Mar Lower Credit Card Fees' },

  { slug: 'La-Jolla-Solana-Payments.html', title: 'La Jolla Solana Payments' },

  { slug: 'Rancho-Santa-Fe-Payment-Processing.html', title: 'Rancho Santa Fe Payment Processing' },

  { slug: 'Same-Day-Payment-Processing.html', title: 'Same Day Payment Processing' },

  { slug: 'Mobile-Payment-Processing.html', title: 'Mobile Payment Processing' },

  { slug: 'Crypto-Payment-Processing.html', title: 'Crypto Payment Processing' },

  { slug: 'Free-Payment-Processing-Setup.html', title: 'Free Payment Processing Setup' },

  { slug: 'Energy-Payments-San-Diego.html', title: 'Energy Payments San Diego' },

  { slug: 'San-Diego-Field-Service-Payments.html', title: 'San Diego Field Service Payments' },

  { slug: 'hvac-payment-processing.html', title: 'Hvac Payment Processing' },

  { slug: 'plumber-payment-processing.html', title: 'Plumber Payment Processing' },

  { slug: 'electrician-payment-processing.html', title: 'Electrician Payment Processing' },

  { slug: 'landscaper-payment-processing.html', title: 'Landscaper Payment Processing' },

  { slug: 'restaurant-payment-processing.html', title: 'Restaurant Payment Processing' },

  { slug: 'restaurant-solana-payments.html', title: 'Restaurant Solana Payments' },

  { slug: 'bar-nightclub-payment-processing.html', title: 'Bar Nightclub Payment Processing' },

  { slug: 'event-ticket-payments.html', title: 'Event Ticket Payments' },

  { slug: 'instant-settlement-api.html', title: 'Instant Settlement Api' },

  { slug: 'solana-pos-terminals.html', title: 'Solana Pos Terminals' },

  { slug: 'usdc-payments-san-diego.html', title: 'Usdc Payments San Diego' },

  { slug: 'subscription-payments-san-diego.html', title: 'Subscription Payments San Diego' },

  { slug: 'invoice-automation-san-diego.html', title: 'Invoice Automation San Diego' },

  { slug: 'payment-integration-services.html', title: 'Payment Integration Services' },

  { slug: 'merchant-account-services.html', title: 'Merchant Account Services' },

  { slug: 'high-risk-payment-processing.html', title: 'High Risk Payment Processing' },

  { slug: 'ac-repair-san-diego.html', title: 'Ac Repair San Diego' },

  { slug: 'why-is-my-ac-not-cooling.html', title: 'Why Is My Ac Not Cooling' },

  { slug: 'ac-making-noise.html', title: 'Ac Making Noise' },

  { slug: 'heater-not-turning-on.html', title: 'Heater Not Turning On' },

  { slug: 'thermostat-not-working.html', title: 'Thermostat Not Working' },

  { slug: 'water-heater-not-working.html', title: 'Water Heater Not Working' },

  { slug: 'no-hot-water-san-diego.html', title: 'No Hot Water San Diego' },

  { slug: 'how-to-fix-slow-drains.html', title: 'How To Fix Slow Drains' },

  { slug: 'why-is-my-toilet-running.html', title: 'Why Is My Toilet Running' },

  { slug: 'water-leak-under-sink.html', title: 'Water Leak Under Sink' },

  { slug: 'roof-leak-after-rain.html', title: 'Roof Leak After Rain' },

  { slug: 'window-wont-close.html', title: 'Window Wont Close' },

  { slug: 'door-wont-latch.html', title: 'Door Wont Latch' },

  { slug: 'garage-door-wont-open.html', title: 'Garage Door Wont Open' },

  { slug: 'power-outage-local-issues.html', title: 'Power Outage Local Issues' },

  { slug: 'circuit-breaker-tripping.html', title: 'Circuit Breaker Tripping' },

  { slug: 'outlet-not-working.html', title: 'Outlet Not Working' },

  { slug: 'flickering-lights-problem.html', title: 'Flickering Lights Problem' },

  { slug: 'wifi-keeps-dropping.html', title: 'Wifi Keeps Dropping' },

  { slug: 'wifi-slow-san-diego.html', title: 'Wifi Slow San Diego' },

  { slug: 'home-network-issues.html', title: 'Home Network Issues' },

  { slug: 'smart-home-not-connecting.html', title: 'Smart Home Not Connecting' },

  { slug: 'tv-mounting-help-near-me.html', title: 'Tv Mounting Help Near Me' },

  { slug: 'foundation-repair-san-diego.html', title: 'Foundation Repair San Diego' },

  { slug: 'foundation-crack-repair.html', title: 'Foundation Crack Repair' },

  { slug: 'retaining-wall-repair.html', title: 'Retaining Wall Repair' },

  { slug: 'emergency-plumber-san-diego.html', title: 'Emergency Plumber San Diego' },

  { slug: 'leak-detection-san-diego.html', title: 'Leak Detection San Diego' },

  { slug: 'sewer-line-repair-san-diego.html', title: 'Sewer Line Repair San Diego' },

  { slug: 'drain-cleaning-san-diego.html', title: 'Drain Cleaning San Diego' },

  { slug: 'water-pressure-low.html', title: 'Water Pressure Low' },

  { slug: 'shower-not-getting-hot.html', title: 'Shower Not Getting Hot' },

  { slug: 'garbage-disposal-jammed.html', title: 'Garbage Disposal Jammed' },

  { slug: 'dishwasher-not-draining.html', title: 'Dishwasher Not Draining' },

  { slug: 'fridge-not-cooling.html', title: 'Fridge Not Cooling' },

  { slug: 'washer-not-spinning.html', title: 'Washer Not Spinning' },

  { slug: 'dryer-not-heating.html', title: 'Dryer Not Heating' },

  { slug: 'landscaping-services-san-diego.html', title: 'Landscaping Services San Diego' },

  { slug: 'tree-removal-san-diego.html', title: 'Tree Removal San Diego' },

  { slug: 'yard-drainage-fix.html', title: 'Yard Drainage Fix' },

  { slug: 'irrigation-system-repair.html', title: 'Irrigation System Repair' },

  { slug: 'sprinklers-not-working.html', title: 'Sprinklers Not Working' },

  { slug: 'gutter-cleaning-san-diego.html', title: 'Gutter Cleaning San Diego' },

  { slug: 'roof-repair-san-diego.html', title: 'Roof Repair San Diego' },

  { slug: 'attic-fan-installation.html', title: 'Attic Fan Installation' },

  { slug: 'home-insulation-san-diego.html', title: 'Home Insulation San Diego' },

  { slug: 'new-window-installation.html', title: 'New Window Installation' },

  { slug: 'garage-conversion-san-diego.html', title: 'Garage Conversion San Diego' },

  { slug: 'furniture-assembly-san-diego.html', title: 'Furniture Assembly San Diego' },

  { slug: 'pest-control-san-diego.html', title: 'Pest Control San Diego' },

  { slug: 'termite-inspection-san-diego.html', title: 'Termite Inspection San Diego' },

  { slug: 'rodent-removal-san-diego.html', title: 'Rodent Removal San Diego' },

  { slug: 'bed-bug-treatment-san-diego.html', title: 'Bed Bug Treatment San Diego' },

  { slug: 'pool-repair-san-diego.html', title: 'Pool Repair San Diego' },

  { slug: 'spa-repair-san-diego.html', title: 'Spa Repair San Diego' },

  { slug: 'water-damage-restoration.html', title: 'Water Damage Restoration' },

  { slug: 'mold-removal-san-diego.html', title: 'Mold Removal San Diego' },

  { slug: 'biohazard-cleanup.html', title: 'Biohazard Cleanup' },

  { slug: 'crime-scene-cleaning.html', title: 'Crime Scene Cleaning' },

  { slug: 'hoarder-cleanup-san-diego.html', title: 'Hoarder Cleanup San Diego' },

  { slug: 'carpet-cleaning-san-diego.html', title: 'Carpet Cleaning San Diego' },

  { slug: 'tile-grout-cleaning-san-diego.html', title: 'Tile Grout Cleaning San Diego' },

  { slug: 'deep-cleaning-services.html', title: 'Deep Cleaning Services' },

  { slug: 'office-cleaning-san-diego.html', title: 'Office Cleaning San Diego' },

  { slug: 'kitchen-remodel-san-diego.html', title: 'Kitchen Remodel San Diego' },

  { slug: 'bathroom-remodel-san-diego.html', title: 'Bathroom Remodel San Diego' }

];

  // add more pages here

];



const template = (title) => `

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>${title} · SideGuy Solutions</title>

</head>

<body>

<h1>${title}</h1>

<p>Auto-generated SideGuy page.</p>

</body>

</html>

`;



pages.forEach((filename) => {

  const title = filename.replace(".html", "").replace(/-/g, " ");

  fs.writeFileSync(filename, template(title));

  console.log("Generated:", filename);

});