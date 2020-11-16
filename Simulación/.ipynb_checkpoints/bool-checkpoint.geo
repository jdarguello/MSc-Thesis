SetFactory("OpenCASCADE");

Point(1) = {0, 0, 0};
Point(2) = {2, 0, 0};
Point(3) = {2, 2, 0};
Point(4) = {0, 2, 0};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Line Loop(1) = {1, 2, 3, 4};

Plane Surface(1) = {1};

Periodic Line{1} = {-3};
Periodic Line{2} = {-4};

Disk(2) = {0, 0, 0, 0.5};
Disk(3) = {2, 0, 0, 0.5};
Disk(4) = {0, 2, 0, 0.5};
Disk(5) = {2, 2, 0, 0.5};
Disk(6) = {1, 1, 0, 0.5};

f1() = BooleanDifference{ Surface{1}; }{ Surface{2:6}; };
f2() = BooleanIntersection{ Surface{1}; Delete; }{ Surface{2:6}; Delete; };
f3() = BooleanUnion{ Surface{ f1() }; Delete; }{ Surface{ f2() }; Delete; }

surfaceVector[] = Extrude {0,0,10} {
 Surface{f3};
};