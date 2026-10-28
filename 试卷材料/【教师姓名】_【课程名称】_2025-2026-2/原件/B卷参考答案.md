【课程名称】B卷参考答案





---

## 一、单选题

1. **B**  
2. **B**  
3. **D**  
4. **C**  
5. **C**

---

## 二、填空题

1. $\displaystyle \frac{\pi}{3}$ 或 $60^\circ$

2. **特征**（特征子空间）

3. $\boxed{5,\,-1,\,-1}$（即 $5$ 单根，$-1$ 二重根）

4. $\boxed{A(k\alpha)=kA(\alpha)}$，其中 $k\in P,\ \alpha\in V$

5. **正交**变换

---

## 三、计算题

### 1. 已知
$$
A=\begin{pmatrix}
1&1&1\\
0&1&1\\
0&0&2
\end{pmatrix}
$$

#### （1）求特征值
因为 $A$ 为上三角矩阵，所以特征值为对角线元素：
$$
\lambda_1=1,\qquad \lambda_2=1,\qquad \lambda_3=2.
$$

#### （2）求每个特征值对应的线性无关特征向量

当 $\lambda=1$ 时：
$$
(A-I)x=0,
$$
$$
A-I=
\begin{pmatrix}
0&1&1\\
0&0&1\\
0&0&1
\end{pmatrix}.
$$
方程组为
$$
x_2+x_3=0,\qquad x_3=0.
$$
因此 $x_3=0,\ x_2=0,\ x_1$ 任意。  
属于 $\lambda=1$ 的线性无关特征向量为
$$
\boxed{\xi_1=(1,0,0)^T}.
$$
注意 $\lambda=1$ 的代数重数为 $2$，但几何重数为 $1$。

当 $\lambda=2$ 时：
$$
(A-2I)x=0,
$$
$$
A-2I=
\begin{pmatrix}
-1&1&1\\
0&-1&1\\
0&0&0
\end{pmatrix}.
$$
方程组为
$$
-x_1+x_2+x_3=0,\qquad -x_2+x_3=0.
$$
由第二式 $x_2=x_3$，代入第一式：
$$
-x_1+x_3+x_3=0\Rightarrow x_1=2x_3.
$$
取 $x_3=1$，得
$$
\boxed{\xi_2=(2,1,1)^T}.
$$

因此：
$$
\boxed{
\lambda=1:\ \xi_1=(1,0,0)^T;\qquad
\lambda=2:\ \xi_2=(2,1,1)^T.
}
$$

#### （3）特征分解

该矩阵只有两个线性无关的特征向量，而矩阵为三阶，因此 **$A$ 不可对角化**。  
所以不存在可逆矩阵 $P$ 和对角矩阵 $\Lambda$ 使
$$
A=P\Lambda P^{-1}.
$$

若写成 Jordan 分解，则可取
$$
P=
\begin{pmatrix}
1&0&2\\
0&1&1\\
0&0&1
\end{pmatrix},
\qquad
J=
\begin{pmatrix}
1&1&0\\
0&1&0\\
0&0&2
\end{pmatrix},
$$
满足
$$
A=PJP^{-1}.
$$
但题目所要求的“对角矩阵 $\Lambda$”不存在。（本小题太难，不写也不扣分）

---

### 2. 将三维向量组化为标准正交基

按图片可辨认的向量组取
$$
\alpha_1=
\begin{pmatrix}1\\1\\1\end{pmatrix},\quad
\alpha_2=
\begin{pmatrix}2\\1\\1\end{pmatrix},\quad
\alpha_3=
\begin{pmatrix}1\\1\\2\end{pmatrix}.
$$
若原卷向量与此不同，请按同样步骤替换计算。

设
$$
v_1=\alpha_1=(1,1,1)^T.
$$
则
$$
u_1=v_1=(1,1,1)^T,
$$
$$
e_1=\frac{u_1}{\|u_1\|}
=\frac{1}{\sqrt3}(1,1,1)^T.
$$

令
$$
u_2=v_2-\frac{(v_2,u_1)}{(u_1,u_1)}u_1.
$$
其中
$$
(v_2,u_1)=2+1+1=4,\qquad (u_1,u_1)=3.
$$
因此
$$
u_2=(2,1,1)^T-\frac43(1,1,1)^T
=\left(\frac23,-\frac13,-\frac13\right)^T.
$$
于是
$$
e_2=\frac{u_2}{\|u_2\|}
=\frac{1}{\sqrt6}(2,-1,-1)^T.
$$

再令
$$
u_3=v_3-\frac{(v_3,u_1)}{(u_1,u_1)}u_1
-\frac{(v_3,u_2)}{(u_2,u_2)}u_2.
$$
计算得
$$
(v_3,u_1)=1+1+2=4,
$$
$$
(v_3,u_2)=1\cdot\frac23+1\cdot\left(-\frac13\right)+2\cdot\left(-\frac13\right)
=-\frac13,
$$
$$
(u_2,u_2)=\frac23.
$$
所以
$$
u_3=(1,1,2)^T-\frac43(1,1,1)^T
-\frac{-1/3}{2/3}u_2
=(0,-\tfrac12,\tfrac12)^T.
$$
于是
$$
e_3=\frac{u_3}{\|u_3\|}
=\frac{1}{\sqrt2}(0,-1,1)^T.
$$

因此一组标准正交基为
$$
\boxed{
e_1=\frac1{\sqrt3}(1,1,1)^T,\quad
e_2=\frac1{\sqrt6}(2,-1,-1)^T,\quad
e_3=\frac1{\sqrt2}(0,-1,1)^T.
}
$$
符号可整体取反，仍为标准正交基。

### 3

在三维线性空间 $\mathbb{R}^3$ 中，已知两组基：
$$
 \begin{cases} \epsilon_1 = (1, 0, 1) \\ \epsilon_2 = (0, 1, 1) \\ \epsilon_3 = (1, 1, 0) \end{cases} \quad \text{和} \quad \begin{cases} \eta_1 = (1, 2, 1) \\ \eta_2 = (0, 1, 2) \\ \eta_3 = (2, 1, 0) \end{cases} 
$$

(1) 求由基 $\epsilon_1, \epsilon_2, \epsilon_3$ 到基 $\eta_1, \eta_2, \eta_3$ 的过渡矩阵；
(2) 求向量 $\xi = (2, 1, 0)$ 在基 $\eta_1, \eta_2, \eta_3$ 下的坐标。

---

### 详细解答

#### (1) 求过渡矩阵

设基 $\epsilon$ 构成的矩阵为 $A = (\epsilon_1, \epsilon_2, \epsilon_3)$，基 $\eta$ 构成的矩阵为 $B = (\eta_1, \eta_2, \eta_3)$。
根据题意：
$$
 A = \begin{pmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 1 & 1 & 0 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 0 & 2 \\ 2 & 1 & 1 \\ 1 & 2 & 0 \end{pmatrix} 
$$

设由基 $\epsilon$ 到基 $\eta$ 的过渡矩阵为 $C$，则有：
$$
 (\eta_1, \eta_2, \eta_3) = (\epsilon_1, \epsilon_2, \epsilon_3)C 
$$
即 $B = AC$。因为 $\epsilon$ 是一组基，矩阵 $A$ 可逆，所以：
$$
 C = A^{-1}B 
$$

为求出 $C$，我们对增广矩阵 $(A | B)$ 进行初等行变换，将其化为 $(I | A^{-1}B)$：
$$
 (A | B) = \left(\begin{array}{ccc|ccc} 1 & 0 & 1 & 1 & 0 & 2 \\ 0 & 1 & 1 & 2 & 1 & 1 \\ 1 & 1 & 0 & 1 & 2 & 0 \end{array}\right) 
$$

**第一步**：将第1行的 $(-1)$ 倍加到第3行 ($r_3 - r_1 \to r_3$)：
$$
 \left(\begin{array}{ccc|ccc} 1 & 0 & 1 & 1 & 0 & 2 \\ 0 & 1 & 1 & 2 & 1 & 1 \\ 0 & 1 & -1 & 0 & 2 & -2 \end{array}\right) 
$$

**第二步**：将第2行的 $(-1)$ 倍加到第3行 ($r_3 - r_2 \to r_3$)：
$$
 \left(\begin{array}{ccc|ccc} 1 & 0 & 1 & 1 & 0 & 2 \\ 0 & 1 & 1 & 2 & 1 & 1 \\ 0 & 0 & -2 & -2 & 1 & -3 \end{array}\right) 
$$

**第三步**：将第3行除以 $(-2)$ ($r_3 \div (-2) \to r_3$)：
$$
 \left(\begin{array}{ccc|ccc} 1 & 0 & 1 & 1 & 0 & 2 \\ 0 & 1 & 1 & 2 & 1 & 1 \\ 0 & 0 & 1 & 1 & -\frac{1}{2} & \frac{3}{2} \end{array}\right) 
$$

**第四步**：消去第3列上方的元素。将第3行的 $(-1)$ 倍加到第1行和第2行 ($r_1 - r_3 \to r_1, r_2 - r_3 \to r_2$)：
$$
 \left(\begin{array}{ccc|ccc} 1 & 0 & 0 & 0 & \frac{1}{2} & \frac{1}{2} \\ 0 & 1 & 0 & 1 & \frac{3}{2} & -\frac{1}{2} \\ 0 & 0 & 1 & 1 & -\frac{1}{2} & \frac{3}{2} \end{array}\right) 
$$

因此，所求的过渡矩阵为：
$$
 \mathbf{C = \begin{pmatrix} 0 & \frac{1}{2} & \frac{1}{2} \\ 1 & \frac{3}{2} & -\frac{1}{2} \\ 1 & -\frac{1}{2} & \frac{3}{2} \end{pmatrix}} 
$$

---

#### (2) 求向量 $\xi$ 在基 $\eta$ 下的坐标

设向量 $\xi$ 在基 $\eta_1, \eta_2, \eta_3$ 下的坐标为 $x = (x_1, x_2, x_3)^T$，则有：
$$
 \xi = (\eta_1, \eta_2, \eta_3)x = Bx 
$$
即解线性方程组 $Bx = \xi$：
$$
 \begin{pmatrix} 1 & 0 & 2 \\ 2 & 1 & 1 \\ 1 & 2 & 0 \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} 2 \\ 1 \\ 0 \end{pmatrix} 
$$

对增广矩阵 $(B | \xi)$ 进行初等行变换：
$$
 \left(\begin{array}{ccc|c} 1 & 0 & 2 & 2 \\ 2 & 1 & 1 & 1 \\ 1 & 2 & 0 & 0 \end{array}\right) 
$$

**第一步**：$r_2 - 2r_1 \to r_2$，$r_3 - r_1 \to r_3$：
$$
 \left(\begin{array}{ccc|c} 1 & 0 & 2 & 2 \\ 0 & 1 & -3 & -3 \\ 0 & 2 & -2 & -2 \end{array}\right) 
$$

**第二步**：$r_3 - 2r_2 \to r_3$：
$$
 \left(\begin{array}{ccc|c} 1 & 0 & 2 & 2 \\ 0 & 1 & -3 & -3 \\ 0 & 0 & 4 & 4 \end{array}\right) 
$$

**第三步**：$r_3 \div 4 \to r_3$：
$$
 \left(\begin{array}{ccc|c} 1 & 0 & 2 & 2 \\ 0 & 1 & -3 & -3 \\ 0 & 0 & 1 & 1 \end{array}\right) 
$$

**第四步**：$r_1 - 2r_3 \to r_1$，$r_2 + 3r_3 \to r_2$：
$$
 \left(\begin{array}{ccc|c} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{array}\right) 
$$
由此解得 $x_1 = 0, x_2 = 0, x_3 = 1$。

所以，向量 $\xi = (2,1,0)$ 在基 $\eta_1, \eta_2, \eta_3$ 下的坐标为：
$$
 \mathbf{(0, 0, 1)^T} 
$$
*(或写成行向量形式 $(0, 0, 1)$ )*



---

### 第4题

**题目：**
设有向量组：
$$
 \begin{cases} \alpha_1 = (1, 2, 0) \\ \alpha_2 = (0, 2, 3) \end{cases} \quad \text{和} \quad \begin{cases} \beta_1 = (2, 3, 1) \\ \beta_2 = (1, 0, -1) \end{cases} 
$$
求由 $\alpha_1, \alpha_2$ 生成的子空间 $L(\alpha_1, \alpha_2)$ 与由 $\beta_1, \beta_2$ 生成的子空间 $L(\beta_1, \beta_2)$ 的交的基与维数。

**详细计算过程：**
设交空间中的任意向量为 $v$，则 $v \in L(\alpha_1, \alpha_2)$ 且 $v \in L(\beta_1, \beta_2)$。
存在常数 $x_1, x_2, y_1, y_2$ 使得：
$$
 v = x_1\alpha_1 + x_2\alpha_2 = y_1\beta_1 + y_2\beta_2 
$$
即：
$$
 x_1\alpha_1 + x_2\alpha_2 - y_1\beta_1 - y_2\beta_2 = 0 
$$
代入具体向量，得到齐次线性方程组：
$$
 x_1 \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix} + x_2 \begin{pmatrix} 0 \\ 2 \\ 3 \end{pmatrix} - y_1 \begin{pmatrix} 2 \\ 3 \\ 1 \end{pmatrix} - y_2 \begin{pmatrix} 1 \\ 0 \\ -1 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix} 
$$
构造系数矩阵并对其进行初等行变换：
$$
 A = \begin{pmatrix} 1 & 0 & -2 & -1 \\ 2 & 2 & -3 & 0 \\ 0 & 3 & -1 & 1 \end{pmatrix} 
$$
将第1行的 $(-2)$ 倍加到第2行（$r_2 - 2r_1 \to r_2$）：
$$
 \begin{pmatrix} 1 & 0 & -2 & -1 \\ 0 & 2 & 1 & 2 \\ 0 & 3 & -1 & 1 \end{pmatrix} 
$$
将第2行乘以 $\frac{1}{2}$，然后第3行减去第2行的 $3$ 倍，或直接进行 $r_3 - \frac{3}{2}r_2 \to r_3$：
$$
 \begin{pmatrix} 1 & 0 & -2 & -1 \\ 0 & 2 & 1 & 2 \\ 0 & 0 & -\frac{5}{2} & -2 \end{pmatrix} 
$$
由最后一行得到方程：$-\frac{5}{2}y_1 - 2y_2 = 0$，即 $5y_1 + 4y_2 = 0$。
令 $y_2 = 5$，则 $y_1 = -4$。
将 $y_1, y_2$ 代入原式，求得交空间中的向量 $v$：
$$
 v = -4\beta_1 + 5\beta_2 = -4(2, 3, 1)^T + 5(1, 0, -1)^T = (-8+5, -12+0, -4-5)^T = (-3, -12, -9)^T 
$$
（可验证：$v = -3\alpha_1 - 3\alpha_2 = -3(1,2,0) - 3(0,2,3) = (-3,-12,-9)$，确实在 $L(\alpha)$ 中）。
由此可知交空间为一维空间，基可以取该向量，为了美观可化简为整数比。

**答案：**
交空间的基为 $\mathbf{(-3, -12, -9)^T}$（或写为成比例的非零向量如 $\mathbf{(1, 4, 3)^T}$），维数为 $\mathbf{1}$。

---

### 第5题

**题目：**
设三阶实对称矩阵
$$
 A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix} 
$$
求正交矩阵 $C$，使得 $C^TAC$ 为对角矩阵，并写出 $C^TAC$ 的矩阵表达式。

**详细计算过程：**
1. **求特征值**：
$$
 |\lambda I - A| = \begin{vmatrix} \lambda-2 & -1 & 0 \\ -1 & \lambda-2 & 0 \\ 0 & 0 & \lambda-3 \end{vmatrix} = (\lambda-3)[(\lambda-2)^2 - 1] = (\lambda-3)(\lambda-1)(\lambda-3) = 0 
$$
特征值为 $\lambda_1 = 1, \lambda_2 = \lambda_3 = 3$。

2. **求特征向量并正交单位化**：
- 对于 $\lambda_1 = 1$：
  $$
 (I - A) = \begin{pmatrix} -1 & -1 & 0 \\ -1 & -1 & 0 \\ 0 & 0 & -2 \end{pmatrix} 
$$
  解得基础解系：$v_1 = (1, -1, 0)^T$。
  单位化得：$e_1 = \frac{1}{\sqrt{2}}(1, -1, 0)^T$。

- 对于 $\lambda_2 = \lambda_3 = 3$：
  $$
 (3I - A) = \begin{pmatrix} 1 & -1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 0 \end{pmatrix} 
$$
  解得基础解系：$v_2 = (1, 1, 0)^T, v_3 = (0, 0, 1)^T$。
  由于 $v_2$ 与 $v_3$ 已经正交，直接单位化得：
  $e_2 = \frac{1}{\sqrt{2}}(1, 1, 0)^T, e_3 = (0, 0, 1)^T$。

3. **构造正交矩阵 $C$**：
将特征向量按列排列：
$$
 C = (e_1, e_2, e_3) = \begin{pmatrix} \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} & 0 \\ -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} & 0 \\ 0 & 0 & 1 \end{pmatrix} 
$$

4. **写出对角矩阵**：
$$
 C^T A C = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 3 \end{pmatrix} 
$$

**答案：**
$$
 \mathbf{C = \begin{pmatrix} \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} & 0 \\ -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} & 0 \\ 0 & 0 & 1 \end{pmatrix}, \quad C^TAC = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 3 \end{pmatrix}} 
$$

---

### 第6题

**题目：**
已知矩阵为
$$
 A = \begin{pmatrix} 1 & 3 & 2 \\ 2 & 8 & 5 \\ 3 & 11 & 13 \end{pmatrix} 
$$
求矩阵的 Doolittle 分解（LU 分解的一种）。要把 $A=LU$ 的矩阵 $L$ 和 $U$ 分别写出来。

**详细计算过程：**
设 $A = LU$，其中 $L$ 为单位下三角矩阵，$U$ 为上三角矩阵：
$$
 \begin{pmatrix} 1 & 3 & 2 \\ 2 & 8 & 5 \\ 3 & 11 & 13 \end{pmatrix} = \begin{pmatrix} 1 & 0 & 0 \\ l_{21} & 1 & 0 \\ l_{31} & l_{32} & 1 \end{pmatrix} \begin{pmatrix} u_{11} & u_{12} & u_{13} \\ 0 & u_{22} & u_{23} \\ 0 & 0 & u_{33} \end{pmatrix} 
$$
按照矩阵乘法逐项求解：
1. **求 $U$ 的第一行**：$u_{11}=1, u_{12}=3, u_{13}=2$。
2. **求 $L$ 的第一列**：$l_{21} = 2/1 = 2$，$l_{31} = 3/1 = 3$。
3. **求 $U$ 的第二行**：
   $l_{21}u_{12} + u_{22} = 8 \implies 2(3) + u_{22} = 8 \implies u_{22} = 2$
   $l_{21}u_{13} + u_{23} = 5 \implies 2(2) + u_{23} = 5 \implies u_{23} = 1$
4. **求 $L$ 的第二列**：
   $l_{31}u_{12} + l_{32}u_{22} = 11 \implies 3(3) + 2l_{32} = 11 \implies 2l_{32} = 2 \implies l_{32} = 1$
5. **求 $U$ 的第三行**：
   $l_{31}u_{13} + l_{32}u_{23} + u_{33} = 13 \implies 3(2) + 1(1) + u_{33} = 13 \implies 6 + 1 + u_{33} = 13 \implies u_{33} = 6$

**答案：**
$$
 \mathbf{L = \begin{pmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ 3 & 1 & 1 \end{pmatrix}, \quad U = \begin{pmatrix} 1 & 3 & 2 \\ 0 & 2 & 1 \\ 0 & 0 & 6 \end{pmatrix}} 
$$

---

### 第7题

**题目：**
设三阶实矩阵
$$
 A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 2 & 3 \\ 1 & 0 & 3 \end{pmatrix} 
$$
有奇异值分解 $A=U\Sigma V^T$，求 $A$ 所有的奇异值并写出矩阵 $\Sigma$。

**详细计算过程：**
计算 $A^TA$ 的特征值，奇异值为特征值的算术平方根。
$$
 A^T A = \begin{pmatrix} 1 & 0 & 1 \\ 2 & 2 & 0 \\ 0 & 3 & 3 \end{pmatrix} \begin{pmatrix} 1 & 2 & 0 \\ 0 & 2 & 3 \\ 1 & 0 & 3 \end{pmatrix} = \begin{pmatrix} 2 & 2 & 3 \\ 2 & 8 & 6 \\ 3 & 6 & 18 \end{pmatrix} 
$$
求 $A^TA$ 的特征多项式：
$$
 |\lambda I - A^T A| = \begin{vmatrix} \lambda-2 & -2 & -3 \\ -2 & \lambda-8 & -6 \\ -3 & -6 & \lambda-18 \end{vmatrix} 
$$
按第一行展开计算：
$$
 = (\lambda-2)[(\lambda-8)(\lambda-18) - 36] + 2[-2(\lambda-18) - 18] - 3[12 - (-3)(\lambda-8)] 
$$
$$
 = (\lambda-2)(\lambda^2 - 26\lambda + 108) + 2(-2\lambda + 18) - 3(3\lambda - 12) 
$$
$$
 = \lambda^3 - 28\lambda^2 + 160\lambda - 216 - 4\lambda + 36 - 9\lambda + 36 
$$
$$
 = \lambda^3 - 28\lambda^2 + 147\lambda - 144 
$$
令特征多项式为 $0$，即 $\lambda^3 - 28\lambda^2 + 147\lambda - 144 = 0$。
*(注：经尝试该三次方程无整数根，若题目原矩阵为 $A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 2 & 3 \\ 1 & 0 & -3 \end{pmatrix}$，则特征值为 21, 7, 0。但基于给定数据，我们求出其无理根即可)*
使用数值方法或卡尔丹公式求解该三次方程可得三个特征值约为：
$$
 \lambda_1 \approx 21.436, \quad \lambda_2 \approx 5.291, \quad \lambda_3 \approx 1.273 
$$
由于 $A$ 是 $3\times 3$ 矩阵，奇异值为 $\sigma_i = \sqrt{\lambda_i}$。
$$
 \sigma_1 \approx 4.63, \quad \sigma_2 \approx 2.30, \quad \sigma_3 \approx 1.13 
$$

**答案：**
奇异值（近似值）为 $\mathbf{\sigma_1 \approx 4.63, \sigma_2 \approx 2.30, \sigma_3 \approx 1.13}$。
由于 $A$ 是 $3\times3$ 的满秩方阵，$\Sigma$ 为对角矩阵：
$$
 \mathbf{\Sigma = \begin{pmatrix} \sigma_1 & 0 & 0 \\ 0 & \sigma_2 & 0 \\ 0 & 0 & \sigma_3 \end{pmatrix}} 
$$
*(注：如果考试时发现方程无整数根，建议直接写出特征方程并以此表示奇异值即可)*。

---

### 第8题

**题目：**
给定矩阵
$$
 A = \begin{pmatrix} 2 & 1 & 1 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix} 
$$
(1) 计算它的代数重数和几何重数，并且判断它是否可以对角化。
(2) 求它的普通特征向量和广义特征向量，并最终写成一个矩阵 $P$。

**详细计算过程：**
(1) **求特征值与重数**：
$A$ 为上三角矩阵，特征值即为对角线元素：$\lambda_1 = 2, \lambda_2 = 2, \lambda_3 = 3$。
- 对于 $\lambda = 2$：
  代数重数 $m_a = 2$。
  计算几何重数：矩阵 $A - 2I = \begin{pmatrix} 0 & 1 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$，显然秩 $r(A-2I) = 2$。
  几何重数 $m_g = n - r = 3 - 2 = 1$。
- 对于 $\lambda = 3$：
  代数重数 $m_a = 1$。
  计算几何重数：$A - 3I = \begin{pmatrix} -1 & 1 & 1 \\ 0 & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix}$，秩 $r(A-3I) = 2$。
  几何重数 $m_g = n - r = 3 - 2 = 1$。
由于 $\lambda=2$ 的代数重数（2）不等于几何重数（1），故 **$A$ 不可对角化**。

(2) **求普通特征向量和广义特征向量**：
- **对于 $\lambda = 2$**：
  普通特征向量：解方程组 $(A - 2I)x = 0$，即：
  $$
 \begin{pmatrix} 0 & 1 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix} 
$$
  得 $x_3 = 0, x_2 = 0$，$x_1$ 自由。取 $x_1=1$，得普通特征向量：
  $$
 v_1 = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} 
$$
  广义特征向量：解方程组 $(A - 2I)x = v_1$，即：
  $$
 \begin{pmatrix} 0 & 1 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} y_1 \\ y_2 \\ y_3 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} 
$$
  得 $y_3 = 0, y_2 = 1$，$y_1$ 自由。取 $y_1 = 0$，得广义特征向量：
  $$
 v_2 = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix} 
$$

- **对于 $\lambda = 3$**：
  普通特征向量：解方程组 $(A - 3I)x = 0$，即：
  $$
 \begin{pmatrix} -1 & 1 & 1 \\ 0 & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix} 
$$
  得 $x_2 = 0$，$-x_1 + x_3 = 0 \implies x_1 = x_3$。取 $x_3 = 1$，得特征向量：
  $$
 v_3 = \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix} 
$$

**答案：**
(1) $\lambda=2$ 的代数重数为 $\mathbf{2}$，几何重数为 $\mathbf{1}$；$\lambda=3$ 的代数重数为 $\mathbf{1}$，几何重数为 $\mathbf{1}$。矩阵 $\mathbf{A}$ **不可以**对角化。
(2) 普通特征向量为 $\mathbf{v_1 = (1, 0, 0)^T}$（对应 $\lambda=2$）和 $\mathbf{v_3 = (1, 0, 1)^T}$（对应 $\lambda=3$），广义特征向量为 $\mathbf{v_2 = (0, 1, 0)^T}$。构成的矩阵 $P$ 为：
$$
 \mathbf{P = (v_1, v_2, v_3) = \begin{pmatrix} 1 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}} 
$$


---

## 四、证明题

### 1. 证明 $\alpha_1,\alpha_2,\alpha_3$ 是一组标准正交基

设 $\varepsilon_1,\varepsilon_2,\varepsilon_3$ 为标准正交基，则
$$
(\varepsilon_i,\varepsilon_j)=\delta_{ij}.
$$
已知
$$
\alpha_1=\frac13(2\varepsilon_1+2\varepsilon_2-\varepsilon_3),
$$
$$
\alpha_2=\frac13(2\varepsilon_1-\varepsilon_2+2\varepsilon_3),
$$
$$
\alpha_3=\frac13(\varepsilon_1-2\varepsilon_2-2\varepsilon_3).
$$

先验证单位长度：
$$
(\alpha_1,\alpha_1)
=\frac19(2^2+2^2+(-1)^2)
=\frac99=1.
$$
同理
$$
(\alpha_2,\alpha_2)
=\frac19(2^2+(-1)^2+2^2)=1,
$$
$$
(\alpha_3,\alpha_3)
=\frac19(1^2+(-2)^2+(-2)^2)=1.
$$

再验证两两正交：
$$
(\alpha_1,\alpha_2)
=\frac19[2\cdot2+2\cdot(-1)+(-1)\cdot2]
=\frac19(4-2-2)=0.
$$
$$
(\alpha_1,\alpha_3)
=\frac19[2\cdot1+2\cdot(-2)+(-1)\cdot(-2)]
=\frac19(2-4+2)=0.
$$
$$
(\alpha_2,\alpha_3)
=\frac19[2\cdot1+(-1)\cdot(-2)+2\cdot(-2)]
=\frac19(2+2-4)=0.
$$

因此
$$
(\alpha_i,\alpha_j)=\delta_{ij}.
$$
又三个向量线性无关，故它们构成三维欧氏空间的一组标准正交基。证毕。

---

### 2. 证明维数公式
$$
\dim(V_1\cap V_2)+\dim((V_1+V_2)\cap V_3)
=\dim(V_2\cap V_3)+\dim((V_2+V_3)\cap V_1).
$$

记
$$
U=V_1+V_2+V_3.
$$
由维数公式
$$
\dim(U)=\dim(V_1+V_2)+\dim V_3-\dim((V_1+V_2)\cap V_3).
$$
又
$$
\dim(V_1+V_2)=\dim V_1+\dim V_2-\dim(V_1\cap V_2),
$$
所以
$$
\dim(U)
=\dim V_1+\dim V_2+\dim V_3
-\dim(V_1\cap V_2)
-\dim((V_1+V_2)\cap V_3). \tag{1}
$$

另一方面，
$$
U=V_1+(V_2+V_3),
$$
由维数公式
$$
\dim(U)=\dim V_1+\dim(V_2+V_3)-\dim((V_2+V_3)\cap V_1).
$$
又
$$
\dim(V_2+V_3)=\dim V_2+\dim V_3-\dim(V_2\cap V_3),
$$
因此
$$
\dim(U)
=\dim V_1+\dim V_2+\dim V_3
-\dim(V_2\cap V_3)
-\dim((V_2+V_3)\cap V_1). \tag{2}
$$

比较 $(1)$ 与 $(2)$，得
$$
\dim(V_1\cap V_2)+\dim((V_1+V_2)\cap V_3)
=\dim(V_2\cap V_3)+\dim((V_2+V_3)\cap V_1).
$$
证毕。