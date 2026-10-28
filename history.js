// Daily Video History Log & Topic Registry
const PODCAST_HISTORY = [
  {
    "episode": 1,
    "topic": "The 'It's Like...' Trap: Mastering Similes for Smoother Comparisons",
    "date": "2026-10-16T03:46:22.027883",
    "duration_sec": 1249.58,
    "duration_min": 20.83,
    "video_file": "podcast_ep1_20261016_032746.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 2,
    "topic": "The 'So...' Spiral: Escaping Repetitive Speech and Sounding More Natural",
    "date": "2026-10-16T12:28:22.220767",
    "duration_sec": 1301.88,
    "duration_min": 21.7,
    "video_file": "podcast_ep2_20261016_121438.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 3,
    "topic": "Stop Saying 'Make' Everything: Unlock 10 Powerful Verbs for Confident English",
    "date": "2026-10-17T11:50:56.474950",
    "duration_sec": 1307.18,
    "duration_min": 21.79,
    "video_file": "podcast_ep3_20261017_113149.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 4,
    "topic": "Beyond 'Very': Supercharging Your Adjectives for Impactful English",
    "date": "2026-10-18T12:15:19.389237",
    "duration_sec": 1285.97,
    "duration_min": 21.43,
    "video_file": "podcast_ep4_20261018_120105.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 5,
    "topic": "From 'Actually...' to Authentic: Charming Your Way Through Conversations",
    "date": "2026-10-19T14:48:31.866137",
    "duration_sec": 1324.92,
    "duration_min": 22.08,
    "video_file": "podcast_ep5_20261019_143333.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 6,
    "topic": "The 'Kind Of' Crutch: Sounding More Decisive and Direct in English",
    "date": "2026-10-20T12:57:35.096572",
    "duration_sec": 1226.09,
    "duration_min": 20.43,
    "video_file": "podcast_ep6_20261020_123934.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 7,
    "topic": "The 'Um...' Abyss: Conquering Hesitation and Sounding Like a Native Speaker",
    "date": "2026-10-21T13:11:04.703862",
    "duration_sec": 1181.47,
    "duration_min": 19.69,
    "video_file": "podcast_ep7_20261021_125143.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 8,
    "topic": "The 'Have To' Hangover: Breaking Free from Obligation and Sounding More Expressive",
    "date": "2026-10-22T13:12:58.642613",
    "duration_sec": 1207.46,
    "duration_min": 20.12,
    "video_file": "podcast_ep8_20261022_125414.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 9,
    "topic": "The 'Just' Jam: How to Sound Less Apologetic and More Assertive",
    "date": "2026-10-23T13:14:17.091726",
    "duration_sec": 1260.43,
    "duration_min": 21.01,
    "video_file": "podcast_ep9_20261023_125434.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 10,
    "topic": "The 'Can I?' Conundrum: Mastering Polite Requests & Confident Asks",
    "date": "2026-10-24T12:23:03.697071",
    "duration_sec": 1241.95,
    "duration_min": 20.7,
    "video_file": "podcast_ep10_20261024_115615.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 11,
    "topic": "The 'Could You?' Conundrum: From Polite Requests to Powerful Influence",
    "date": "2026-10-25T12:56:04.242168",
    "duration_sec": 1307.52,
    "duration_min": 21.79,
    "video_file": "podcast_ep11_20261025_122821.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 12,
    "topic": "The 'Like, Totally!' Loophole: Escaping Overused Fillers and Sounding Effortlessly Cool",
    "date": "2026-10-26T14:35:15.935476",
    "duration_sec": 1323.29,
    "duration_min": 22.05,
    "video_file": "podcast_ep12_20261026_140530.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 13,
    "topic": "The 'Go' Get-Up: Unlocking 10 Dynamic Verbs to Replace Generic 'Go' Sentences",
    "date": "2026-10-27T13:33:52.312887",
    "duration_sec": 1405.63,
    "duration_min": 23.43,
    "video_file": "podcast_ep13_20261027_130626.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 14,
    "topic": "The 'I Think That...' Tangle: Unraveling Tentative Talk for Clearer Confidence",
    "date": "2026-10-28T14:24:06.546296",
    "duration_sec": 1329.0,
    "duration_min": 22.15,
    "video_file": "podcast_ep14_20261028_135708.mp4",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
