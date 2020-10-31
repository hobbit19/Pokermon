use crate::features::Features;
use crate::hand::HoleCards;
use lazy_static::lazy_static;
use rs_poker::core::{Card, Suit, Value};

lazy_static! {
    pub static ref ALL_CARDS: Vec<Card> = {
        let mut cards: Vec<Card> = vec![];
        for value in Value::values().iter() {
            for suit in Suit::suits().iter() {
                cards.push(Card {
                    value: *value,
                    suit: *suit,
                })
            }
        }
        cards
    };
}

lazy_static! {
    pub static ref ALL_HANDS: Vec<HoleCards> = {
        let mut hands: Vec<HoleCards> = vec![];
        for i in 0..ALL_CARDS.len() {
            for j in i + 1..ALL_CARDS.len() {
                hands.push(HoleCards::new_from_cards(ALL_CARDS[i], ALL_CARDS[j]));
            }
        }
        hands
    };
}

lazy_static! {
    pub static ref PREFLOP_HAND_FEATURES: Vec<(i32, &'static str, f32, f32, f32)> = vec![
        (0, "22o", 0.4938, 0.0189, 0.4873),
        (1, "32s", 0.3309, 0.0578, 0.6113),
        (2, "32o", 0.2923, 0.0612, 0.6465),
        (3, "33o", 0.5283, 0.0170, 0.4547),
        (4, "42s", 0.3391, 0.0582, 0.6027),
        (5, "42o", 0.3011, 0.0616, 0.6373),
        (6, "43s", 0.3572, 0.0582, 0.5846),
        (7, "43o", 0.3206, 0.0615, 0.6179),
        (8, "44o", 0.5625, 0.0153, 0.4222),
        (9, "52s", 0.3492, 0.0583, 0.5925),
        (10, "52o", 0.3119, 0.0618, 0.6263),
        (11, "53s", 0.3675, 0.0586, 0.5739),
        (12, "53o", 0.3316, 0.0619, 0.6065),
        (13, "54s", 0.3853, 0.0584, 0.5563),
        (14, "54o", 0.3507, 0.0616, 0.5877),
        (15, "55o", 0.5964, 0.0136, 0.3900),
        (16, "62s", 0.3483, 0.0566, 0.5951),
        (17, "62o", 0.3107, 0.0599, 0.6294),
        (18, "63s", 0.3668, 0.0569, 0.5763),
        (19, "63o", 0.3306, 0.0601, 0.6093),
        (20, "64s", 0.3848, 0.0570, 0.5582),
        (21, "64o", 0.3500, 0.0601, 0.5899),
        (22, "65s", 0.4034, 0.0557, 0.5409),
        (23, "65o", 0.3701, 0.0586, 0.5713),
        (24, "66o", 0.6270, 0.0116, 0.3614),
        (25, "72s", 0.3543, 0.0543, 0.5914),
        (26, "72o", 0.3171, 0.0574, 0.6255),
        (27, "73s", 0.3730, 0.0546, 0.5724),
        (28, "73o", 0.3371, 0.0576, 0.6053),
        (29, "74s", 0.3910, 0.0548, 0.5542),
        (30, "74o", 0.3566, 0.0577, 0.5857),
        (31, "75s", 0.4097, 0.0539, 0.5364),
        (32, "75o", 0.3767, 0.0567, 0.5666),
        (33, "76s", 0.4282, 0.0508, 0.5210),
        (34, "76o", 0.3965, 0.0533, 0.5502),
        (35, "77o", 0.6572, 0.0102, 0.3326),
        (36, "82s", 0.3767, 0.0518, 0.5715),
        (37, "82o", 0.3408, 0.0548, 0.6044),
        (38, "83s", 0.3828, 0.0518, 0.5654),
        (39, "83o", 0.3474, 0.0546, 0.5980),
        (40, "84s", 0.4010, 0.0519, 0.5471),
        (41, "84o", 0.3670, 0.0547, 0.5783),
        (42, "85s", 0.4199, 0.0510, 0.5291),
        (43, "85o", 0.3874, 0.0537, 0.5589),
        (44, "86s", 0.4381, 0.0484, 0.5135),
        (45, "86o", 0.4069, 0.0508, 0.5423),
        (46, "87s", 0.4568, 0.0450, 0.4982),
        (47, "87o", 0.4269, 0.0471, 0.5260),
        (48, "88o", 0.6871, 0.0089, 0.3040),
        (49, "92s", 0.3997, 0.0488, 0.5515),
        (50, "92o", 0.3651, 0.0516, 0.5833),
        (51, "93s", 0.4080, 0.0491, 0.5429),
        (52, "93o", 0.3742, 0.0518, 0.5740),
        (53, "94s", 0.4140, 0.0490, 0.5370),
        (54, "94o", 0.3808, 0.0517, 0.5675),
        (55, "95s", 0.4331, 0.0481, 0.5188),
        (56, "95o", 0.4013, 0.0506, 0.5481),
        (57, "96s", 0.4515, 0.0455, 0.5030),
        (58, "96o", 0.4210, 0.0477, 0.5313),
        (59, "97s", 0.4699, 0.0425, 0.4876),
        (60, "97o", 0.4407, 0.0445, 0.5148),
        (61, "98s", 0.4885, 0.0388, 0.4727),
        (62, "98o", 0.4606, 0.0405, 0.4989),
        (63, "99o", 0.7166, 0.0078, 0.2756),
        (64, "T2s", 0.4254, 0.0459, 0.5287),
        (65, "T2o", 0.3923, 0.0485, 0.5592),
        (66, "T3s", 0.4337, 0.0462, 0.5201),
        (67, "T3o", 0.4015, 0.0487, 0.5498),
        (68, "T4s", 0.4420, 0.0465, 0.5115),
        (69, "T4o", 0.4105, 0.0489, 0.5406),
        (70, "T5s", 0.4493, 0.0455, 0.5052),
        (71, "T5o", 0.4185, 0.0478, 0.5337),
        (72, "T6s", 0.4680, 0.0428, 0.4892),
        (73, "T6o", 0.4384, 0.0448, 0.5168),
        (74, "T7s", 0.4865, 0.0397, 0.4738),
        (75, "T7o", 0.4582, 0.0415, 0.5003),
        (76, "T8s", 0.5050, 0.0365, 0.4585),
        (77, "T8o", 0.4781, 0.0380, 0.4839),
        (78, "T9s", 0.5237, 0.0330, 0.4433),
        (79, "T9o", 0.4981, 0.0343, 0.4676),
        (80, "TTo", 0.7466, 0.0070, 0.2464),
        (81, "J2s", 0.4520, 0.0435, 0.5045),
        (82, "J2o", 0.4204, 0.0459, 0.5337),
        (83, "J3s", 0.4604, 0.0437, 0.4959),
        (84, "J3o", 0.4296, 0.0461, 0.5243),
        (85, "J4s", 0.4686, 0.0440, 0.4874),
        (86, "J4o", 0.4386, 0.0463, 0.5151),
        (87, "J5s", 0.4782, 0.0433, 0.4785),
        (88, "J5o", 0.4490, 0.0455, 0.5055),
        (89, "J6s", 0.4857, 0.0406, 0.4737),
        (90, "J6o", 0.4571, 0.0426, 0.5003),
        (91, "J7s", 0.5045, 0.0374, 0.4581),
        (92, "J7o", 0.4772, 0.0391, 0.4837),
        (93, "J8s", 0.5231, 0.0340, 0.4429),
        (94, "J8o", 0.4971, 0.0355, 0.4674),
        (95, "J9s", 0.5411, 0.0310, 0.4279),
        (96, "J9o", 0.5163, 0.0322, 0.4515),
        (97, "JTs", 0.5615, 0.0274, 0.4111),
        (98, "JTo", 0.5382, 0.0284, 0.4334),
        (99, "JJo", 0.7715, 0.0063, 0.2222),
        (100, "Q2s", 0.4810, 0.0413, 0.4777),
        (101, "Q2o", 0.4510, 0.0437, 0.5053),
        (102, "Q3s", 0.4893, 0.0416, 0.4691),
        (103, "Q3o", 0.4602, 0.0438, 0.4960),
        (104, "Q4s", 0.4976, 0.0418, 0.4606),
        (105, "Q4o", 0.4692, 0.0440, 0.4868),
        (106, "Q5s", 0.5071, 0.0411, 0.4518),
        (107, "Q5o", 0.4795, 0.0432, 0.4773),
        (108, "Q6s", 0.5167, 0.0386, 0.4447),
        (109, "Q6o", 0.4899, 0.0405, 0.4696),
        (110, "Q7s", 0.5252, 0.0355, 0.4393),
        (111, "Q7o", 0.4990, 0.0372, 0.4638),
        (112, "Q8s", 0.5441, 0.0320, 0.4239),
        (113, "Q8o", 0.5193, 0.0333, 0.4474),
        (114, "Q9s", 0.5622, 0.0288, 0.4090),
        (115, "Q9o", 0.5386, 0.0299, 0.4315),
        (116, "QTs", 0.5817, 0.0259, 0.3924),
        (117, "QTo", 0.5594, 0.0268, 0.4138),
        (118, "QJs", 0.5907, 0.0237, 0.3856),
        (119, "QJo", 0.5690, 0.0245, 0.4065),
        (120, "QQo", 0.7963, 0.0058, 0.1979),
        (121, "K2s", 0.5123, 0.0394, 0.4483),
        (122, "K2o", 0.4842, 0.0417, 0.4741),
        (123, "K3s", 0.5207, 0.0396, 0.4397),
        (124, "K3o", 0.4933, 0.0418, 0.4649),
        (125, "K4s", 0.5288, 0.0399, 0.4313),
        (126, "K4o", 0.5022, 0.0420, 0.4558),
        (127, "K5s", 0.5383, 0.0391, 0.4226),
        (128, "K5o", 0.5125, 0.0412, 0.4463),
        (129, "K6s", 0.5480, 0.0367, 0.4153),
        (130, "K6o", 0.5229, 0.0385, 0.4386),
        (131, "K7s", 0.5584, 0.0338, 0.4078),
        (132, "K7o", 0.5341, 0.0354, 0.4305),
        (133, "K8s", 0.5679, 0.0304, 0.4017),
        (134, "K8o", 0.5443, 0.0317, 0.4240),
        (135, "K9s", 0.5863, 0.0270, 0.3867),
        (136, "K9o", 0.5640, 0.0280, 0.4080),
        (137, "KTs", 0.6058, 0.0240, 0.3702),
        (138, "KTo", 0.5849, 0.0248, 0.3903),
        (139, "KJs", 0.6147, 0.0218, 0.3635),
        (140, "KJo", 0.5944, 0.0225, 0.3831),
        (141, "KQs", 0.6240, 0.0198, 0.3562),
        (142, "KQo", 0.6043, 0.0204, 0.3753),
        (143, "KKo", 0.8211, 0.0055, 0.1734),
        (144, "A2s", 0.5550, 0.0374, 0.4076),
        (145, "A2o", 0.5294, 0.0396, 0.4310),
        (146, "A3s", 0.5633, 0.0377, 0.3990),
        (147, "A3o", 0.5385, 0.0397, 0.4218),
        (148, "A4s", 0.5713, 0.0379, 0.3908),
        (149, "A4o", 0.5473, 0.0399, 0.4128),
        (150, "A5s", 0.5806, 0.0371, 0.3823),
        (151, "A5o", 0.5574, 0.0390, 0.4036),
        (152, "A6s", 0.5817, 0.0345, 0.3838),
        (153, "A6o", 0.5587, 0.0362, 0.4051),
        (154, "A7s", 0.5938, 0.0319, 0.3743),
        (155, "A7o", 0.5716, 0.0334, 0.3950),
        (156, "A8s", 0.6050, 0.0287, 0.3663),
        (157, "A8o", 0.5837, 0.0299, 0.3864),
        (158, "A9s", 0.6150, 0.0254, 0.3596),
        (159, "A9o", 0.5944, 0.0264, 0.3792),
        (160, "ATs", 0.6348, 0.0222, 0.3430),
        (161, "ATo", 0.6156, 0.0230, 0.3614),
        (162, "AJs", 0.6439, 0.0199, 0.3362),
        (163, "AJo", 0.6253, 0.0205, 0.3542),
        (164, "AQs", 0.6531, 0.0179, 0.3290),
        (165, "AQo", 0.6350, 0.0184, 0.3466),
        (166, "AKs", 0.6621, 0.0165, 0.3214),
        (167, "AKo", 0.6446, 0.0170, 0.3384),
        (168, "AAo", 0.8493, 0.0054, 0.1453),
    ];
}
