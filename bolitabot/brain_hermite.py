import torch

def get_hermite_point(t_val, p0_list, p1_list, v0_list, v1_list):
    def to_list(x):
        try:
            return [float(v) for v in x]
        except:
            return [float(x[0]), float(x[1])]

    t = torch.tensor(float(t_val), dtype=torch.float32, requires_grad=True)
    p0 = torch.tensor(to_list(p0_list), dtype=torch.float32)
    p1 = torch.tensor(to_list(p1_list), dtype=torch.float32)
    v0 = torch.tensor(to_list(v0_list), dtype=torch.float32)
    v1 = torch.tensor(to_list(v1_list), dtype=torch.float32)

    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2

    pos = h00 * p0 + h10 * v0 + h01 * p1 + h11 * v1
    px, py = pos[0], pos[1]

    vx = torch.autograd.grad(px, t, create_graph=True)[0]
    vy = torch.autograd.grad(py, t, create_graph=True)[0]

    ax = torch.autograd.grad(vx, t)[0]
    ay = torch.autograd.grad(vy, t)[0]

    return (
        float(px.detach().item()),
        float(py.detach().item()),
        float(vx.detach().item()),
        float(vy.detach().item()),
        float(ax.detach().item()),
        float(ay.detach().item())
    )