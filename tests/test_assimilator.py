import dolfin
import fixtures

from pulse_adjoint import (  # Regularization,; StrainObservation,
    Assimilator,
    BoundaryObservation,
    OptimizationTarget,
    VolumeObservation,
)

# import numpy as np
# import pytest
# from pulse import HeartGeometry


def main():

    problem, control = fixtures.create_problem()
    geo = problem.geometry
    V_cg2 = dolfin.VectorFunctionSpace(geo.mesh, "CG", 2)
    u = dolfin.Function(V_cg2)
    volume_obs = VolumeObservation(
        mesh=geo.mesh, dmu=geo.ds(geo.markers["ENDO"]), description="Test LV volume"
    )

    model_volume = volume_obs(u).vector().get_local()[0]
    print(model_volume)
    volumes = (2.7, 2.9)
    # volumes = (2.7,)
    target = OptimizationTarget(volumes, volume_obs, collect=True)

    lvp = [0.5, 1.0]
    # lvp = [0.5]
    bcs = BoundaryObservation(bc=problem.bcs.neumann[0], data=lvp)

    assimilator = Assimilator(problem, target, bcs, control)
    assimilator.assimilate()

    from IPython import embed

    embed()
    exit()


if __name__ == "__main__":
    main()
