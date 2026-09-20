document.addEventListener("DOMContentLoaded", function () {
    if (typeof DateTimeShortcuts === "undefined") {
        return;
    }

    DateTimeShortcuts.clockHours.default_ = [
        ["Now", -1],
        ["Midnight", 0],
        ["1 a.m.", 1],
        ["2 a.m.", 2],
        ["3 a.m.", 3],
        ["4 a.m.", 4],
        ["5 a.m.", 5],
        ["6 a.m.", 6],
        ["7 a.m.", 7],
        ["8 a.m.", 8],
        ["9 a.m.", 9],
        ["10 a.m.", 10],
        ["11 a.m.", 11],
        ["Noon", 12],
        ["1 p.m.", 13],
        ["2 p.m.", 14],
        ["3 p.m.", 15],
        ["4 p.m.", 16],
        ["5 p.m.", 17],
        ["6 p.m.", 18],
        ["7 p.m.", 19],
        ["8 p.m.", 20],
        ["9 p.m.", 21],
        ["10 p.m.", 22],
        ["11 p.m.", 23],
    ];
});
