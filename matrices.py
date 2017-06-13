import numpy as np


def perspective(fov, ratio, near, far):
    zmul = (-2.0 * near * far) / (far - near)
    ymul = 1.0 / np.tan(fov * np.pi / 360.0)
    xmul = ymul / ratio
    return np.matrix([
        [xmul, 0.0, 0.0, 0.0],
        [0.0, ymul, 0.0, 0.0],
        [0.0, 0.0, -1.0, zmul],
        [0.0, 0.0, -1.0, 0.0],
    ])


def lookat(eye, target, up=(0.0, 0.0, 1.0)):
    eye = np.array(eye)
    target = np.array(target)
    up = np.array(up)

    forward = target - eye
    forward /= np.linalg.norm(forward)

    side = np.cross(forward, up)
    side /= np.linalg.norm(side)

    upward = np.cross(side, forward)
    upward /= np.linalg.norm(upward)

    return np.matrix([
        [side[0], side[1], side[2], -np.dot(eye, side)],
        [upward[0], upward[1], upward[2], -np.dot(eye, upward)],
        [-forward[0], -forward[1], -forward[2], np.dot(eye, forward)],
        [0.0, 0.0, 0.0, 1.0],
    ])


def create_mvp(proj, view):
    return np.transpose(proj @ view).astype(np.float32)
