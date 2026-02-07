# CS2402 Assignment 1 完成指南（不含代码）

本指南基于 `Assignment_01/cs2402-a1-72401030.ipynb` 的任务说明，按作业结构逐步引导完成。遵守作业规则：只能使用 `numpy`（仅基础数组与 `np.random.rand/seed`）、`matplotlib.pyplot`、`math`、`scipy.stats`（仅用于理论曲线）。禁止使用任何高层分布生成器。

## 0. 准备与检查
- 确认 `STUDENT_ID` 已设置为你的学号。
- 在每次运行前设置随机种子为 `STUDENT_ID`，保证结果可复现。
- 牢记最后一位学号决定正态分布公式的 `cos` 或 `sin` 版本（奇数用 `cos`，偶数用 `sin`）。

## 1. 参数生成（已给出）
- `get_parameters` 会根据学号生成 `binom_n, binom_p, uni_a, uni_b, exp_lam, norm_mu, norm_sigma`。
- 你只需调用此函数，不要改动其逻辑。

## 2. 四个分布的“从零实现”思路
以下只给方法与逻辑，不给具体代码。

### 2.1 Binomial(n, p) —— 方法 2（伯努利试验求和）
要求：不能使用逆变换法。
- 对于每一个样本：进行 `n` 次独立伯努利试验。
- 每次试验使用 `U~Uniform(0,1)`，若 `U<p` 记为成功(1)，否则失败(0)。
- 将 `n` 次结果相加得到一个样本值。
- 重复 `size` 次得到样本列表/数组。
- 建议用二维随机矩阵 `size x n`，再按行计数成功次数（可用循环或向量化）。

### 2.2 Uniform(a, b) —— 线性变换
- 使用 `U~Uniform(0,1)`。
- 线性变换：`X = a + (b-a) * U`。
- 生成 `size` 个样本即可。

### 2.3 Exponential(λ) —— 逆变换法
- 设 `U~Uniform(0,1)`，令 `F(X)=U`。
- 解方程：`F(X)=1-exp(-λX)=U` → `X = -ln(1-U)/λ`。
- 代码中通常用 `-np.log(1-U)/lam`。
- 注意：`U` 不能为 0；`np.random.rand()` 返回值在 (0,1) 内，满足要求。

### 2.4 Normal(μ, σ²) —— Box-Muller
- 生成 `U1, U2 ~ Uniform(0,1)`。
- 标准公式：
  - `Z0 = sqrt(-2 ln U1) * cos(2π U2)`
  - `Z1 = sqrt(-2 ln U1) * sin(2π U2)`
- 依据学号最后一位选择 `Z0` 或 `Z1`。
- 最后线性变换得到 `X = μ + σ * Z`。

## 3. 主程序与可视化（2x2 子图）
完成 `main()` 的思路：
1. 调用 `get_parameters(STUDENT_ID)`。
2. `np.random.seed(STUDENT_ID)`。
3. 设置 `N_SAMPLES = 1000`（可提高到 10000 观察平滑效果）。
4. 调用四个生成器得到四组样本。
5. 用 `plt.subplots(2,2)`，顺序严格遵循：
   - 左上：Binomial
   - 右上：Exponential
   - 左下：Normal
   - 右下：Uniform
6. 每个子图：
   - 先画直方图（`density=True`）。
   - 再叠加理论 PMF/PDF：
     - Binomial：`stats.binom.pmf(k, n, p)`，`k` 用整数范围。
     - Exponential：`stats.expon.pdf(x, scale=1/lam)`，注意 `scale`。
     - Normal：`stats.norm.pdf(x, loc=mu, scale=sigma)`。
     - Uniform：`stats.uniform.pdf(x, loc=a, scale=b-a)`。

## 4. Part 2：数学推导与解释（需要文字+公式）

### 4.1 Exponential 逆变换推导
需要写：
1. 从 `F(X)=U` 推导 `X` 的过程：
   - `1 - exp(-λX) = U`
   - `exp(-λX) = 1 - U`
   - `-λX = ln(1-U)`
   - `X = -ln(1-U)/λ`
2. 编程解释：为何要 `np.log(1-U)`，说明对指数方程取对数才能解出 `X`。

### 4.2 Box-Muller 正态推导
需要写：
1. 两个方程（`Z0, Z1`），用 LaTeX。
2. 结合学号说明：
   - 你选用的是 `Z0` 还是 `Z1`（cos 或 sin）。
   - 如果用了另一个，也仍然是 `N(0,1)`，因为两者都来自同一 Box-Muller 推导且独立同分布。

## 5. 常见检查点
- 是否误用 `np.random.normal/binomial/exponential` 等被禁函数。
- 是否忘记 `density=True`，导致理论曲线不匹配。
- Exponential 的理论曲线是否正确设置 `scale=1/λ`。
- 正态变换是否正确使用 `μ + σ Z`。
- 子图顺序是否与要求一致。

## 6. 提交前自检
- 运行一遍 `main()`，确认图像正常显示。
- 确认 Part 2 的文字解释完整、公式正确、能对应到代码。
- 不要在代码中出现被禁函数名。

如果你希望，我可以根据你写好的文字或图像结果再帮你做查错与改进建议（不代写代码）。
