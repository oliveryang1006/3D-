const state = {
    orders: [
        {
            id: 'A2306',
            title: '居家康复护理 · 周全服务',
            area: '朝阳区',
            type: '康复护理',
            assignable: false,
            time: '2024-06-12 14:00',
            org: '颐康养老服务中心',
            status: '待机构确认',
        },
        {
            id: 'B1468',
            title: '陪诊服务 · 三甲医院',
            area: '浦东新区',
            type: '陪诊',
            assignable: true,
            time: '2024-06-12 09:00',
            org: '芦苇志愿服务站',
            status: '志愿者待指派',
        },
        {
            id: 'C9931',
            title: '助餐助浴 · 日常照护',
            area: '高新区',
            type: '家政',
            assignable: false,
            time: '2024-06-13 10:30',
            org: '松语护理中心',
            status: '义工待接单',
        },
        {
            id: 'D7780',
            title: '心理陪伴 · 每周两次',
            area: '浦东新区',
            type: '陪诊',
            assignable: true,
            time: '2024-06-14 15:00',
            org: '邻里守护社工站',
            status: '志愿者招募中',
        },
    ],
};

const roleTabs = document.querySelectorAll('.role-tab');
const rolePanels = document.querySelectorAll('.role-panel');
const orderListEl = document.querySelector('.order-list');
const filterArea = document.querySelector('#filter-area');
const filterType = document.querySelector('#filter-type');
const togglePersonal = document.querySelector('#toggle-personal');
const dialog = document.querySelector('.form-dialog');
const overlay = document.querySelector('.overlay');
const dialogContent = document.querySelector('.dialog-content');
const templateRoot = document.querySelector('#form-templates');
const dialogClose = document.querySelector('.dialog-close');
const menuToggle = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('.mobile-nav');

function renderOrders() {
    if (!orderListEl) return;

    const area = filterArea.value;
    const type = filterType.value;
    const personalOnly = togglePersonal.checked;

    orderListEl.innerHTML = '';

    const filtered = state.orders.filter((order) => {
        const areaMatch = area === 'all' || order.area === area;
        const typeMatch = type === 'all' || order.type === type;
        const assignMatch = !personalOnly || order.assignable;
        return areaMatch && typeMatch && assignMatch;
    });

    if (!filtered.length) {
        orderListEl.innerHTML = '<p class="empty">暂无符合条件的订单。</p>';
        return;
    }

    const fragment = document.createDocumentFragment();

    filtered.forEach((order) => {
        const card = document.createElement('article');
        card.className = 'order-card';
        card.innerHTML = `
            <span class="tag">${order.assignable ? '志愿者可接' : '机构派单'}</span>
            <h3>${order.title}</h3>
            <p class="order-meta">订单编号：${order.id}</p>
            <p class="order-meta">服务时间：${order.time}</p>
            <p class="order-meta">服务区域：${order.area}</p>
            <p class="order-meta">派单机构：${order.org}</p>
            <p class="order-status">当前状态：${order.status}</p>
            <div class="order-actions">
                <button class="btn ghost" data-form="view-order" data-order="${order.id}">详情</button>
                <button class="btn primary" data-form="${order.assignable ? 'apply-volunteer' : 'claim-volunteer'}" data-order="${order.id}">
                    ${order.assignable ? '申请参与' : '提交接单申请'}
                </button>
            </div>
        `;
        fragment.appendChild(card);
    });

    orderListEl.appendChild(fragment);
}

function openDialog(formName, dataset = {}) {
    const template = templateRoot.content.querySelector(`section[data-form="${formName}"]`);

    if (!template) {
        dialogContent.innerHTML = `<p>功能开发中，敬请期待。</p>`;
    } else {
        dialogContent.innerHTML = template.outerHTML;
        const form = dialogContent.querySelector('form');
        if (form && dataset.order) {
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'orderId';
            hiddenInput.value = dataset.order;
            form.appendChild(hiddenInput);
        }
    }

    dialog.showModal();
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
}

function closeDialog() {
    dialog.close();
    overlay.hidden = true;
    dialogContent.innerHTML = '';
    document.body.style.overflow = '';
}

function handleTabClick(event) {
    const { role } = event.currentTarget.dataset;
    roleTabs.forEach((tab) => {
        const isActive = tab.dataset.role === role;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });

    rolePanels.forEach((panel) => {
        panel.classList.toggle('active', panel.dataset.role === role);
    });
}

function handleActionClick(event) {
    const target = event.target.closest('[data-form]');
    if (!target) return;

    const { form, order } = target.dataset;

    if (form === 'view-order') {
        const orderInfo = state.orders.find((item) => item.id === order);
        if (!orderInfo) return;

        dialogContent.innerHTML = `
            <section>
                <h2>订单详情 · ${orderInfo.id}</h2>
                <p><strong>服务主题：</strong>${orderInfo.title}</p>
                <p><strong>服务时间：</strong>${orderInfo.time}</p>
                <p><strong>服务区域：</strong>${orderInfo.area}</p>
                <p><strong>派单机构：</strong>${orderInfo.org}</p>
                <p><strong>当前状态：</strong>${orderInfo.status}</p>
                <p>志愿者可接：${orderInfo.assignable ? '是' : '否（需机构派单）'}</p>
            </section>
        `;
        dialog.showModal();
        overlay.hidden = false;
        document.body.style.overflow = 'hidden';
        return;
    }

    if (['apply-volunteer', 'claim-volunteer'].includes(form)) {
        openDialog(orderInfoFor(form), { order });
        return;
    }

    openDialog(form, { order });
}

function orderInfoFor(form) {
    return form === 'apply-volunteer' ? 'signup-volunteer' : 'login-volunteer';
}

roleTabs.forEach((tab) => tab.addEventListener('click', handleTabClick));
document.addEventListener('click', handleActionClick);
[filterArea, filterType, togglePersonal].forEach((input) => input?.addEventListener('change', renderOrders));
dialogClose?.addEventListener('click', closeDialog);
overlay?.addEventListener('click', closeDialog);
dialog?.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeDialog();
});

menuToggle?.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
});

mobileNav?.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        mobileNav.classList.remove('open');
    }
});

renderOrders();
