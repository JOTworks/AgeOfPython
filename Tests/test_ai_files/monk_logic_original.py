(defconst monk-target 99)
(defconst gl-local-total 100)
(defconst gl-local-last 101)
(defconst gl-remote-total 102)
(defconst gl-remote-last 103)

(defrule
(true)
=>
(set-goal monk-target -1)
(disable-self)
)


(defrule
    (building-type-count monastery < 1)
=>
(build monastery)
)


(defrule
(can-research ri-redemption)
=>
(research ri-redemption)
)


(defrule
    (unit-type-count-total monk < 1)
    (can-train monk)
=>
(train monk)
)


(defrule
    (goal monk-target -1)
=>
(chat-to-all "looking")
    (up-reset-search 1 1 1 1)
    (up-find-local c: monk c: 1)
(set-strategic-number sn-focus-player-number 2) ;needs to be not hard coded
(up-find-remote c: stable c: 1)
    (up-get-search-state gl-local-total))

(defrule
(up-compare-goal gl-remote-total > 0); Found stable
=>
(chat-to-all "found stable"))

(defrule
(up-compare-goal gl-local-total > 0); Found monk
=>
(chat-to-all "found monk"))


(defrule
    (up-compare-goal gl-remote-total > 0); Found stable
       (up-compare-goal gl-local-total > 0); Found monk
            (goal monk-target -1)

=>
(chat-to-all "converting")
    (up-set-target-object search-remote c: 0)
    (up-target-objects 0 action-default -1 -1))