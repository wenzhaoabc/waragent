| Interaction   | Form    | Parameters       |
|---------------|---------------------------|----------------------|
| Bond Length   | $E_{\text{bond}}(r) = \frac{1}{2} K_b (r - r_0)^2$ |$K_b = 350.0 \, \text{kcal/mol}, \, r_0 = 1.53 \, \text{Å}$|
| Bond Angle    |$E_{\text{angle}}(\theta) = \frac{1}{2} K_\theta (\theta - \theta_0)^2$ |$K_\theta = 60 \, \text{kcal/mol/rad}^2, \, \theta_0 = 1.911 \, \text{rad} \, (109.5^\circ)$|
| Dihedral Angle|$E_{\text{dihedral}}(\phi) = \sum_{i=0}^{n} C_i \cos(i\phi)$|$C_0 = 1.736, \, C_1 = -4.490, \, C_2 = 0.776, \, C_3 = 6.990 \, (\text{kcal/mol})$ |
| Non-bonded    |$E_{\text{non-bonding}}(r) = 4\epsilon \left[ \left( \frac{\sigma}{r} \right)^{12} - \left( \frac{\sigma}{r} \right)^6 \right], \, r \leq r_c$|$\sigma = 4.01 \, \text{Å}, \, \epsilon = 0.112 \, \text{kcal/mol}$  |