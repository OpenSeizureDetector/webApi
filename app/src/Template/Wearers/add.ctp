<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Wearer $wearer
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('List Wearers'), ['action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Datapoints'), ['controller' => 'Datapoints', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Datapoint'), ['controller' => 'Datapoints', 'action' => 'add']) ?></li>
    </ul>
</nav>
<div class="wearers form large-9 medium-8 columns content">
    <?= $this->Form->create($wearer) ?>
    <fieldset>
        <legend><?= __('Add Wearer') ?></legend>
        <?php
            echo $this->Form->control('name');
            echo $this->Form->control('dob', ['empty' => true]);
            echo $this->Form->control('ald');
            echo $this->Form->control('user_id', ['options' => $users]);
        ?>
    </fieldset>
    <?= $this->Form->button(__('Submit')) ?>
    <?= $this->Form->end() ?>
</div>
