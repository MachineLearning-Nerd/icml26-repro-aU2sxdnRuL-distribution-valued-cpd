# Limitations and deviations

- This is a full mechanism audit, not a reproduction of Table 1 performance.
- The controlled distributions are Gaussian affine pushforwards, not either real-world case study.
- The source equations are reconstructed in NumPy; parity with the released R/funcharts implementation is a separate verification route.
- Six of 600 empirical transports are independently solved from dense cost matrices. Optimality for the remainder follows from the same predeclared positive-diagonal convex-gradient construction.
- The historical uncentered-field control is not used: for this exact compatible barycenter construction, the sample mean displacement is zero, so that control is mathematically incapable of separating implementations.
