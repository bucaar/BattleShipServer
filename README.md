# BattleShip

### To run the server
 * `git clone "https://github.com/bucaar/BattleShipServer.git"`
 * `cd BattleShipServer`
 * `chmod u+x ./game.py`
 * `./game.py`

### BATTLESHIP PROTOCOL

| Variable | Datatype | Valid values |
| --- | --- | --- |
| **ship_id** | string | "C", "B", "S", "D", "P" |
| **x** | int | [ 0 - 9 ] |
| **y** | int | [ 0 - 9 ] |
| **orient** | string | "h", "v" |
| **result** | string | "HIT", "MISS", "SUNK" |
| **message** | string | |

| From Server | Reply type | Description |
| --- | --- | --- |
| NAME | string | String containing the desired username |
| SHIP PLACEMENT | json | {**ship_id**: [**x**, **y**, **orient**]} |
| SHOT LOCATION | json | [**x**, **y**] |
| **result** | | Result of previous SHOT LOCATION message |
| OPPONENT SHOT **x**,**y**,**result** | | Notification of opponent's action |
| WIN | | Notification of winning the game |
| LOSE | | Notification of losing the game |
| ERROR **message** | | Notification of error occuring |

