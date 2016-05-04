/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                       */
/*  \   \        Copyright (c) 2003-2009 Xilinx, Inc.                */
/*  /   /          All Right Reserved.                                 */
/* /---/   /\                                                         */
/* \   \  /  \                                                      */
/*  \___\/\___\                                                    */
/***********************************************************************/

/* This file is designed for use with ISim build 0x7708f090 */

#define XSI_HIDE_SYMBOL_SPEC true
#include "xsi.h"
#include <memory.h>
#ifdef __GNUC__
#include <stdlib.h>
#else
#include <malloc.h>
#define alloca _alloca
#endif
static const char *ng0 = "D:/OneDrive/Projects/CS240/lab72/calc.v";
static int ng1[] = {0, 0};
static int ng2[] = {1, 0};
static int ng3[] = {3, 0};
static int ng4[] = {4, 0};
static int ng5[] = {5, 0};
static int ng6[] = {2, 0};



static void Always_13_0(char *t0)
{
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t5;
    char *t6;
    char *t7;

LAB0:    t1 = (t0 + 4288U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(13, ng0);
    t2 = (t0 + 5104);
    *((int *)t2) = 1;
    t3 = (t0 + 4320);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB4;

LAB1:    return;
LAB4:    xsi_set_current_line(13, ng0);

LAB5:    xsi_set_current_line(14, ng0);
    t4 = (t0 + 2408);
    t5 = (t4 + 56U);
    t6 = *((char **)t5);
    t7 = (t0 + 2248);
    xsi_vlogvar_wait_assign_value(t7, t6, 0, 0, 2, 1000LL);
    xsi_set_current_line(15, ng0);
    t2 = (t0 + 2728);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t5, t4, 0, 0, 8, 1000LL);
    xsi_set_current_line(16, ng0);
    t2 = (t0 + 3208);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 3048);
    xsi_vlogvar_wait_assign_value(t5, t4, 0, 0, 3, 1000LL);
    xsi_set_current_line(17, ng0);
    t2 = (t0 + 1368U);
    t3 = *((char **)t2);
    t2 = (t0 + 3368);
    xsi_vlogvar_wait_assign_value(t2, t3, 0, 0, 1, 1000LL);
    xsi_set_current_line(18, ng0);
    t2 = (t0 + 2888);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 2088);
    xsi_vlogvar_wait_assign_value(t5, t4, 0, 0, 8, 1000LL);
    goto LAB2;

}

static void Cont_21_1(char *t0)
{
    char t4[8];
    char t15[8];
    char t36[8];
    char t44[8];
    char *t1;
    char *t2;
    char *t3;
    unsigned int t5;
    unsigned int t6;
    unsigned int t7;
    unsigned int t8;
    unsigned int t9;
    char *t10;
    char *t11;
    unsigned int t12;
    unsigned int t13;
    unsigned int t14;
    char *t16;
    char *t17;
    char *t18;
    char *t19;
    unsigned int t20;
    unsigned int t21;
    unsigned int t22;
    unsigned int t23;
    unsigned int t24;
    char *t25;
    char *t26;
    char *t27;
    unsigned int t28;
    unsigned int t29;
    unsigned int t30;
    unsigned int t31;
    unsigned int t32;
    unsigned int t33;
    unsigned int t34;
    unsigned int t35;
    char *t37;
    unsigned int t38;
    unsigned int t39;
    unsigned int t40;
    unsigned int t41;
    unsigned int t42;
    char *t43;
    unsigned int t45;
    unsigned int t46;
    unsigned int t47;
    char *t48;
    char *t49;
    char *t50;
    unsigned int t51;
    unsigned int t52;
    unsigned int t53;
    unsigned int t54;
    unsigned int t55;
    unsigned int t56;
    unsigned int t57;
    char *t58;
    char *t59;
    unsigned int t60;
    unsigned int t61;
    unsigned int t62;
    unsigned int t63;
    unsigned int t64;
    unsigned int t65;
    unsigned int t66;
    unsigned int t67;
    int t68;
    int t69;
    unsigned int t70;
    unsigned int t71;
    unsigned int t72;
    unsigned int t73;
    unsigned int t74;
    unsigned int t75;
    char *t76;
    char *t77;
    char *t78;
    char *t79;
    char *t80;
    unsigned int t81;
    unsigned int t82;
    char *t83;
    unsigned int t84;
    unsigned int t85;
    char *t86;
    unsigned int t87;
    unsigned int t88;
    char *t89;

LAB0:    t1 = (t0 + 4536U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(21, ng0);
    t2 = (t0 + 1368U);
    t3 = *((char **)t2);
    memset(t4, 0, 8);
    t2 = (t3 + 4);
    t5 = *((unsigned int *)t2);
    t6 = (~(t5));
    t7 = *((unsigned int *)t3);
    t8 = (t7 & t6);
    t9 = (t8 & 1U);
    if (t9 != 0)
        goto LAB4;

LAB5:    if (*((unsigned int *)t2) != 0)
        goto LAB6;

LAB7:    t11 = (t4 + 4);
    t12 = *((unsigned int *)t4);
    t13 = *((unsigned int *)t11);
    t14 = (t12 || t13);
    if (t14 > 0)
        goto LAB8;

LAB9:    memcpy(t44, t4, 8);

LAB10:    t76 = (t0 + 5216);
    t77 = (t76 + 56U);
    t78 = *((char **)t77);
    t79 = (t78 + 56U);
    t80 = *((char **)t79);
    memset(t80, 0, 8);
    t81 = 1U;
    t82 = t81;
    t83 = (t44 + 4);
    t84 = *((unsigned int *)t44);
    t81 = (t81 & t84);
    t85 = *((unsigned int *)t83);
    t82 = (t82 & t85);
    t86 = (t80 + 4);
    t87 = *((unsigned int *)t80);
    *((unsigned int *)t80) = (t87 | t81);
    t88 = *((unsigned int *)t86);
    *((unsigned int *)t86) = (t88 | t82);
    xsi_driver_vfirst_trans(t76, 0, 0);
    t89 = (t0 + 5120);
    *((int *)t89) = 1;

LAB1:    return;
LAB4:    *((unsigned int *)t4) = 1;
    goto LAB7;

LAB6:    t10 = (t4 + 4);
    *((unsigned int *)t4) = 1;
    *((unsigned int *)t10) = 1;
    goto LAB7;

LAB8:    t16 = (t0 + 3368);
    t17 = (t16 + 56U);
    t18 = *((char **)t17);
    memset(t15, 0, 8);
    t19 = (t18 + 4);
    t20 = *((unsigned int *)t19);
    t21 = (~(t20));
    t22 = *((unsigned int *)t18);
    t23 = (t22 & t21);
    t24 = (t23 & 1U);
    if (t24 != 0)
        goto LAB14;

LAB12:    if (*((unsigned int *)t19) == 0)
        goto LAB11;

LAB13:    t25 = (t15 + 4);
    *((unsigned int *)t15) = 1;
    *((unsigned int *)t25) = 1;

LAB14:    t26 = (t15 + 4);
    t27 = (t18 + 4);
    t28 = *((unsigned int *)t18);
    t29 = (~(t28));
    *((unsigned int *)t15) = t29;
    *((unsigned int *)t26) = 0;
    if (*((unsigned int *)t27) != 0)
        goto LAB16;

LAB15:    t34 = *((unsigned int *)t15);
    *((unsigned int *)t15) = (t34 & 1U);
    t35 = *((unsigned int *)t26);
    *((unsigned int *)t26) = (t35 & 1U);
    memset(t36, 0, 8);
    t37 = (t15 + 4);
    t38 = *((unsigned int *)t37);
    t39 = (~(t38));
    t40 = *((unsigned int *)t15);
    t41 = (t40 & t39);
    t42 = (t41 & 1U);
    if (t42 != 0)
        goto LAB17;

LAB18:    if (*((unsigned int *)t37) != 0)
        goto LAB19;

LAB20:    t45 = *((unsigned int *)t4);
    t46 = *((unsigned int *)t36);
    t47 = (t45 & t46);
    *((unsigned int *)t44) = t47;
    t48 = (t4 + 4);
    t49 = (t36 + 4);
    t50 = (t44 + 4);
    t51 = *((unsigned int *)t48);
    t52 = *((unsigned int *)t49);
    t53 = (t51 | t52);
    *((unsigned int *)t50) = t53;
    t54 = *((unsigned int *)t50);
    t55 = (t54 != 0);
    if (t55 == 1)
        goto LAB21;

LAB22:
LAB23:    goto LAB10;

LAB11:    *((unsigned int *)t15) = 1;
    goto LAB14;

LAB16:    t30 = *((unsigned int *)t15);
    t31 = *((unsigned int *)t27);
    *((unsigned int *)t15) = (t30 | t31);
    t32 = *((unsigned int *)t26);
    t33 = *((unsigned int *)t27);
    *((unsigned int *)t26) = (t32 | t33);
    goto LAB15;

LAB17:    *((unsigned int *)t36) = 1;
    goto LAB20;

LAB19:    t43 = (t36 + 4);
    *((unsigned int *)t36) = 1;
    *((unsigned int *)t43) = 1;
    goto LAB20;

LAB21:    t56 = *((unsigned int *)t44);
    t57 = *((unsigned int *)t50);
    *((unsigned int *)t44) = (t56 | t57);
    t58 = (t4 + 4);
    t59 = (t36 + 4);
    t60 = *((unsigned int *)t4);
    t61 = (~(t60));
    t62 = *((unsigned int *)t58);
    t63 = (~(t62));
    t64 = *((unsigned int *)t36);
    t65 = (~(t64));
    t66 = *((unsigned int *)t59);
    t67 = (~(t66));
    t68 = (t61 & t63);
    t69 = (t65 & t67);
    t70 = (~(t68));
    t71 = (~(t69));
    t72 = *((unsigned int *)t50);
    *((unsigned int *)t50) = (t72 & t70);
    t73 = *((unsigned int *)t50);
    *((unsigned int *)t50) = (t73 & t71);
    t74 = *((unsigned int *)t44);
    *((unsigned int *)t44) = (t74 & t70);
    t75 = *((unsigned int *)t44);
    *((unsigned int *)t44) = (t75 & t71);
    goto LAB23;

}

static void Always_23_2(char *t0)
{
    char t21[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t5;
    char *t6;
    char *t7;
    unsigned int t8;
    unsigned int t9;
    unsigned int t10;
    unsigned int t11;
    unsigned int t12;
    int t13;
    char *t14;
    char *t15;
    int t16;
    char *t17;
    char *t18;
    char *t19;
    char *t20;
    char *t22;

LAB0:    t1 = (t0 + 4784U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(23, ng0);
    t2 = (t0 + 5136);
    *((int *)t2) = 1;
    t3 = (t0 + 4816);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB4;

LAB1:    return;
LAB4:    xsi_set_current_line(23, ng0);

LAB5:    xsi_set_current_line(24, ng0);
    t4 = (t0 + 2248);
    t5 = (t4 + 56U);
    t6 = *((char **)t5);
    t7 = (t0 + 2408);
    xsi_vlogvar_assign_value(t7, t6, 0, 0, 2);
    xsi_set_current_line(25, ng0);
    t2 = (t0 + 2568);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 2728);
    xsi_vlogvar_assign_value(t5, t4, 0, 0, 8);
    xsi_set_current_line(26, ng0);
    t2 = (t0 + 3048);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 3208);
    xsi_vlogvar_assign_value(t5, t4, 0, 0, 3);
    xsi_set_current_line(27, ng0);
    t2 = (t0 + 2088);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = (t0 + 2888);
    xsi_vlogvar_assign_value(t5, t4, 0, 0, 8);
    xsi_set_current_line(28, ng0);
    t2 = (t0 + 1208U);
    t3 = *((char **)t2);
    t2 = (t3 + 4);
    t8 = *((unsigned int *)t2);
    t9 = (~(t8));
    t10 = *((unsigned int *)t3);
    t11 = (t10 & t9);
    t12 = (t11 != 0);
    if (t12 > 0)
        goto LAB6;

LAB7:    xsi_set_current_line(33, ng0);

LAB10:    xsi_set_current_line(34, ng0);
    t2 = (t0 + 2248);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);

LAB11:    t5 = ((char*)((ng1)));
    t13 = xsi_vlog_unsigned_case_compare(t4, 2, t5, 32);
    if (t13 == 1)
        goto LAB12;

LAB13:    t2 = ((char*)((ng2)));
    t13 = xsi_vlog_unsigned_case_compare(t4, 2, t2, 32);
    if (t13 == 1)
        goto LAB14;

LAB15:    t2 = ((char*)((ng6)));
    t13 = xsi_vlog_unsigned_case_compare(t4, 2, t2, 32);
    if (t13 == 1)
        goto LAB16;

LAB17:
LAB18:
LAB8:    goto LAB2;

LAB6:    xsi_set_current_line(28, ng0);

LAB9:    xsi_set_current_line(29, ng0);
    t4 = ((char*)((ng1)));
    t5 = (t0 + 2408);
    xsi_vlogvar_assign_value(t5, t4, 0, 0, 2);
    xsi_set_current_line(30, ng0);
    t2 = ((char*)((ng1)));
    t3 = (t0 + 2728);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 8);
    xsi_set_current_line(31, ng0);
    t2 = ((char*)((ng1)));
    t3 = (t0 + 3208);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 3);
    xsi_set_current_line(32, ng0);
    t2 = ((char*)((ng1)));
    t3 = (t0 + 2888);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 8);
    goto LAB8;

LAB12:    xsi_set_current_line(35, ng0);

LAB19:    xsi_set_current_line(36, ng0);
    t6 = (t0 + 1688U);
    t7 = *((char **)t6);
    t6 = (t7 + 4);
    t8 = *((unsigned int *)t6);
    t9 = (~(t8));
    t10 = *((unsigned int *)t7);
    t11 = (t10 & t9);
    t12 = (t11 != 0);
    if (t12 > 0)
        goto LAB20;

LAB21:
LAB22:    goto LAB18;

LAB14:    xsi_set_current_line(42, ng0);

LAB24:    xsi_set_current_line(43, ng0);
    t3 = (t0 + 1688U);
    t5 = *((char **)t3);
    t3 = (t5 + 4);
    t8 = *((unsigned int *)t3);
    t9 = (~(t8));
    t10 = *((unsigned int *)t5);
    t11 = (t10 & t9);
    t12 = (t11 != 0);
    if (t12 > 0)
        goto LAB25;

LAB26:
LAB27:    goto LAB18;

LAB16:    xsi_set_current_line(59, ng0);

LAB49:    xsi_set_current_line(60, ng0);
    t3 = (t0 + 1688U);
    t5 = *((char **)t3);
    t3 = (t5 + 4);
    t8 = *((unsigned int *)t3);
    t9 = (~(t8));
    t10 = *((unsigned int *)t5);
    t11 = (t10 & t9);
    t12 = (t11 != 0);
    if (t12 > 0)
        goto LAB50;

LAB51:
LAB52:    goto LAB18;

LAB20:    xsi_set_current_line(36, ng0);

LAB23:    xsi_set_current_line(37, ng0);
    t14 = ((char*)((ng2)));
    t15 = (t0 + 2408);
    xsi_vlogvar_assign_value(t15, t14, 0, 0, 2);
    xsi_set_current_line(38, ng0);
    t2 = (t0 + 1528U);
    t3 = *((char **)t2);
    t2 = (t0 + 2728);
    xsi_vlogvar_assign_value(t2, t3, 0, 0, 8);
    xsi_set_current_line(39, ng0);
    t2 = (t0 + 1528U);
    t3 = *((char **)t2);
    t2 = (t0 + 2888);
    xsi_vlogvar_assign_value(t2, t3, 0, 0, 8);
    goto LAB22;

LAB25:    xsi_set_current_line(43, ng0);

LAB28:    xsi_set_current_line(44, ng0);
    t6 = (t0 + 1528U);
    t7 = *((char **)t6);

LAB29:    t6 = ((char*)((ng3)));
    t16 = xsi_vlog_unsigned_case_compare(t7, 8, t6, 32);
    if (t16 == 1)
        goto LAB30;

LAB31:    t2 = ((char*)((ng4)));
    t13 = xsi_vlog_unsigned_case_compare(t7, 8, t2, 32);
    if (t13 == 1)
        goto LAB32;

LAB33:    t2 = ((char*)((ng5)));
    t13 = xsi_vlog_unsigned_case_compare(t7, 8, t2, 32);
    if (t13 == 1)
        goto LAB34;

LAB35:
LAB37:
LAB36:    xsi_set_current_line(48, ng0);

LAB39:    xsi_set_current_line(49, ng0);
    t2 = (t0 + 1528U);
    t3 = *((char **)t2);
    t2 = (t0 + 2888);
    xsi_vlogvar_assign_value(t2, t3, 0, 0, 8);
    xsi_set_current_line(50, ng0);
    t2 = (t0 + 1528U);
    t3 = *((char **)t2);
    t2 = ((char*)((ng3)));
    memset(t21, 0, 8);
    t5 = (t3 + 4);
    if (*((unsigned int *)t5) != 0)
        goto LAB41;

LAB40:    t6 = (t2 + 4);
    if (*((unsigned int *)t6) != 0)
        goto LAB41;

LAB44:    if (*((unsigned int *)t3) < *((unsigned int *)t2))
        goto LAB42;

LAB43:    t15 = (t21 + 4);
    t8 = *((unsigned int *)t15);
    t9 = (~(t8));
    t10 = *((unsigned int *)t21);
    t11 = (t10 & t9);
    t12 = (t11 != 0);
    if (t12 > 0)
        goto LAB45;

LAB46:    xsi_set_current_line(54, ng0);
    t2 = ((char*)((ng2)));
    t3 = (t0 + 2408);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 2);

LAB47:
LAB38:    goto LAB27;

LAB30:    xsi_set_current_line(45, ng0);
    t14 = (t0 + 2568);
    t15 = (t14 + 56U);
    t17 = *((char **)t15);
    t18 = (t0 + 2568);
    t19 = (t18 + 56U);
    t20 = *((char **)t19);
    memset(t21, 0, 8);
    xsi_vlog_unsigned_multiply(t21, 8, t17, 8, t20, 8);
    t22 = (t0 + 2888);
    xsi_vlogvar_assign_value(t22, t21, 0, 0, 8);
    goto LAB38;

LAB32:    xsi_set_current_line(46, ng0);
    t3 = (t0 + 2568);
    t5 = (t3 + 56U);
    t6 = *((char **)t5);
    t14 = ((char*)((ng2)));
    memset(t21, 0, 8);
    xsi_vlog_unsigned_add(t21, 32, t6, 8, t14, 32);
    t15 = (t0 + 2888);
    xsi_vlogvar_assign_value(t15, t21, 0, 0, 8);
    goto LAB38;

LAB34:    xsi_set_current_line(47, ng0);
    t3 = (t0 + 2568);
    t5 = (t3 + 56U);
    t6 = *((char **)t5);
    t14 = ((char*)((ng2)));
    memset(t21, 0, 8);
    xsi_vlog_unsigned_minus(t21, 32, t6, 8, t14, 32);
    t15 = (t0 + 2888);
    xsi_vlogvar_assign_value(t15, t21, 0, 0, 8);
    goto LAB38;

LAB41:    t14 = (t21 + 4);
    *((unsigned int *)t21) = 1;
    *((unsigned int *)t14) = 1;
    goto LAB43;

LAB42:    *((unsigned int *)t21) = 1;
    goto LAB43;

LAB45:    xsi_set_current_line(50, ng0);

LAB48:    xsi_set_current_line(51, ng0);
    t17 = ((char*)((ng6)));
    t18 = (t0 + 2408);
    xsi_vlogvar_assign_value(t18, t17, 0, 0, 2);
    xsi_set_current_line(52, ng0);
    t2 = (t0 + 1528U);
    t3 = *((char **)t2);
    t2 = (t0 + 3208);
    xsi_vlogvar_assign_value(t2, t3, 0, 0, 3);
    goto LAB47;

LAB50:    xsi_set_current_line(60, ng0);

LAB53:    xsi_set_current_line(61, ng0);
    t6 = ((char*)((ng1)));
    t14 = (t0 + 2408);
    xsi_vlogvar_assign_value(t14, t6, 0, 0, 2);
    xsi_set_current_line(62, ng0);
    t2 = (t0 + 3048);
    t3 = (t2 + 56U);
    t5 = *((char **)t3);

LAB54:    t6 = ((char*)((ng1)));
    t13 = xsi_vlog_unsigned_case_compare(t5, 3, t6, 32);
    if (t13 == 1)
        goto LAB55;

LAB56:    t2 = ((char*)((ng2)));
    t13 = xsi_vlog_unsigned_case_compare(t5, 3, t2, 32);
    if (t13 == 1)
        goto LAB57;

LAB58:    t2 = ((char*)((ng6)));
    t13 = xsi_vlog_unsigned_case_compare(t5, 3, t2, 32);
    if (t13 == 1)
        goto LAB59;

LAB60:
LAB61:    goto LAB52;

LAB55:    xsi_set_current_line(63, ng0);
    t14 = (t0 + 2568);
    t15 = (t14 + 56U);
    t17 = *((char **)t15);
    t18 = (t0 + 1528U);
    t19 = *((char **)t18);
    memset(t21, 0, 8);
    xsi_vlog_unsigned_multiply(t21, 8, t17, 8, t19, 8);
    t18 = (t0 + 2888);
    xsi_vlogvar_assign_value(t18, t21, 0, 0, 8);
    goto LAB61;

LAB57:    xsi_set_current_line(64, ng0);
    t3 = (t0 + 2568);
    t6 = (t3 + 56U);
    t14 = *((char **)t6);
    t15 = (t0 + 1528U);
    t17 = *((char **)t15);
    memset(t21, 0, 8);
    xsi_vlog_unsigned_add(t21, 8, t14, 8, t17, 8);
    t15 = (t0 + 2888);
    xsi_vlogvar_assign_value(t15, t21, 0, 0, 8);
    goto LAB61;

LAB59:    xsi_set_current_line(65, ng0);
    t3 = (t0 + 2568);
    t6 = (t3 + 56U);
    t14 = *((char **)t6);
    t15 = (t0 + 1528U);
    t17 = *((char **)t15);
    memset(t21, 0, 8);
    xsi_vlog_unsigned_minus(t21, 8, t14, 8, t17, 8);
    t15 = (t0 + 2888);
    xsi_vlogvar_assign_value(t15, t21, 0, 0, 8);
    goto LAB61;

}


extern void work_m_00000000002389600995_4061625060_init()
{
	static char *pe[] = {(void *)Always_13_0,(void *)Cont_21_1,(void *)Always_23_2};
	xsi_register_didat("work_m_00000000002389600995_4061625060", "isim/calc_tb_isim_beh.exe.sim/work/m_00000000002389600995_4061625060.didat");
	xsi_register_executes(pe);
}
