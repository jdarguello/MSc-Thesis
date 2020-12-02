#include "createRDeltaT.H"

Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

#include "createPhi.H"


label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, pimple.dict(), pRefCell, pRefValue);
mesh.setFluxRequired(p.name());


singlePhaseTransportModel laminarTransport(U, phi);

autoPtr<incompressible::momentumTransportModel> turbulence
(
    incompressible::momentumTransportModel::New(U, phi, laminarTransport)
);

#include "createMRF.H"

Info« "Reading transportProperties\n" « endl;

IOdictionary transportProperties
(
    IOobject
        (
            "transportProperties",
            runTime.constant(),
            mesh,
            IOobject::MUST_READ_IF_MODIFIED,
            IOobject::NO_WRITE
        )
);
dimensionedScalar rhoInfValue
(
    transportProperties.lookup("rhoInf")
);
dimensionedScalar invrhoInf("invrhoInf",(1.0/rhoInfValue));


volScalarField rhoInf
(
    IOobject
        (
            "rho",
            runTime.timeName(),
            mesh,
            IOobject::NO_READ,
            IOobject::AUTO_WRITE
        ),
    mesh,
    rhoInfValue
);

volScalarField mu
(
    IOobject
        (
            "mu",
            runTime.timeName(),
            mesh,
            IOobject::NO_READ,
            IOobject::AUTO_WRITE
        ),
    laminarTransport.nu()
    *rhoInfValue
);

const word kinematicCloudName
(
    args.optionLookupOrDefault<word>("cloudName", "kinematicCloud")
);
Info« "Constructing kinematicCloud " « kinematicCloudName « endl;
basicKinematicCollidingCloud kinematicCloud
(
    kinematicCloudName,
    rhoInf,
    U,
    mu,
    g
);

#include "createFvOptions.H"