<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Wearer[]|\Cake\Collection\CollectionInterface $wearers
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('New Wearer'), ['action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Datapoints'), ['controller' => 'Datapoints', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Datapoint'), ['controller' => 'Datapoints', 'action' => 'add']) ?></li>
    </ul>
</nav>
<div class="wearers index large-9 medium-8 columns content">
    <h3><?= __('Wearers') ?></h3>
    <table cellpadding="0" cellspacing="0">
        <thead>
            <tr>
                <th scope="col"><?= $this->Paginator->sort('id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('name') ?></th>
                <th scope="col"><?= $this->Paginator->sort('dob') ?></th>
                <th scope="col"><?= $this->Paginator->sort('ald') ?></th>
                <th scope="col"><?= $this->Paginator->sort('user_id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('created') ?></th>
                <th scope="col"><?= $this->Paginator->sort('modified') ?></th>
                <th scope="col" class="actions"><?= __('Actions') ?></th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($wearers as $wearer): ?>
            <tr>
                <td><?= $this->Number->format($wearer->id) ?></td>
                <td><?= h($wearer->name) ?></td>
                <td><?= h($wearer->dob) ?></td>
                <td><?= h($wearer->ald) ?></td>
                <td><?= $wearer->has('user') ? $this->Html->link($wearer->user->id, ['controller' => 'Users', 'action' => 'view', $wearer->user->id]) : '' ?></td>
                <td><?= h($wearer->created) ?></td>
                <td><?= h($wearer->modified) ?></td>
                <td class="actions">
                    <?= $this->Html->link(__('View'), ['action' => 'view', $wearer->id]) ?>
                    <?= $this->Html->link(__('Edit'), ['action' => 'edit', $wearer->id]) ?>
                    <?= $this->Form->postLink(__('Delete'), ['action' => 'delete', $wearer->id], ['confirm' => __('Are you sure you want to delete # {0}?', $wearer->id)]) ?>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <div class="paginator">
        <ul class="pagination">
            <?= $this->Paginator->first('<< ' . __('first')) ?>
            <?= $this->Paginator->prev('< ' . __('previous')) ?>
            <?= $this->Paginator->numbers() ?>
            <?= $this->Paginator->next(__('next') . ' >') ?>
            <?= $this->Paginator->last(__('last') . ' >>') ?>
        </ul>
        <p><?= $this->Paginator->counter(['format' => __('Page {{page}} of {{pages}}, showing {{current}} record(s) out of {{count}} total')]) ?></p>
    </div>
</div>
