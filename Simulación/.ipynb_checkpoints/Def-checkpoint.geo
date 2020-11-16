SetFactory("OpenCASCADE");

Mesh.CharacteristicLengthMin = 0.1;
Mesh.CharacteristicLengthMax = 0.1;

s0 = news;
Rectangle(s0) = {-1.0, -1.0, 0.0, 2.0, 2.0};

s1 = news;
Disk(s1) = {-1.0, 0.0, 0.0, 0.5};

s2 = news;
Disk(s2) = {1.0, 0.0, 0.0, 0.5};

bo1[] = BooleanUnion{Surface {s0}; Delete;} {Surface {s1,s2}; Delete;};

ex1[] = Extrude{0,0,1}{Surface{bo1};};